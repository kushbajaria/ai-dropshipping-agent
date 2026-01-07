# Production Deployment & Monitoring Guide

## 1. DEPLOYMENT ARCHITECTURE

### Recommended Stack
```
Frontend (Next.js/React)
    ↓
CDN (CloudFlare)
    ↓
Load Balancer (Application Load Balancer)
    ↓
FastAPI Backend (Docker containers)
    ↓
PostgreSQL RDS
    ↓
Redis ElastiCache
    ↓
Storage (S3 for backups/logs)
```

### Infrastructure as Code (Terraform)
```hcl
# backend/infrastructure/main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# RDS PostgreSQL
resource "aws_rds_cluster" "main" {
  cluster_identifier      = "ai-dropshipping-prod"
  engine                  = "aurora-postgresql"
  engine_version          = "15.2"
  database_name           = "dropshipping"
  master_username         = "admin"
  master_password         = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.main.name
  db_cluster_parameter_group_name = "default.aurora-postgresql15"
  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"
  skip_final_snapshot     = false
  deletion_protection     = true
  
  tags = {
    Name = "ai-dropshipping-db"
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "main" {
  cluster_id           = "ai-dropshipping-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  
  tags = {
    Name = "ai-dropshipping-cache"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "ai-dropshipping-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  tags = {
    Name = "ai-dropshipping-alb"
  }
}
```

---

## 2. DOCKER DEPLOYMENT

### Dockerfile
```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Run migrations and start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### Docker Compose (Local Development)
```yaml
# docker-compose.yml

version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: dropshipping
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/dropshipping
      REDIS_HOST: redis
      REDIS_PORT: 6379
      SECRET_KEY: ${SECRET_KEY}
      STRIPE_SECRET_KEY: ${STRIPE_SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app

volumes:
  postgres_data:
```

---

## 3. DATABASE MIGRATIONS (Alembic)

### Setup
```bash
cd backend
alembic init migrations
```

### Create Migration
```bash
alembic revision --autogenerate -m "Add user table"
```

### Apply Migrations
```python
# backend/app/migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.models import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")

    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
```

---

## 4. MONITORING & LOGGING

### Application Monitoring (Sentry)
```python
# backend/app/main.py

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,
    environment=os.getenv("ENVIRONMENT", "development"),
    release=os.getenv("APP_VERSION", "unknown")
)
```

### Structured Logging
```python
# backend/app/logging_config.py

import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger("app")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger
```

### Performance Monitoring
```python
# backend/app/middleware/performance.py

from time import time
from fastapi import Request

@app.middleware("http")
async def log_performance(request: Request, call_next):
    start = time()
    response = await call_next(request)
    duration = time() - start
    
    logger.info(
        "request_completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": int(duration * 1000),
        }
    )
    
    # Alert if slow
    if duration > 1.0:
        logger.warning(f"Slow request: {request.method} {request.url.path} took {duration}s")
    
    return response
```

---

## 5. HEALTH CHECKS & READINESS

```python
# backend/app/routes/health.py

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
import redis

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "ok"}

@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check - verify all dependencies are working"""
    checks = {
        "database": False,
        "redis": False,
        "api": True
    }
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception as e:
        logger.error(f"Database check failed: {e}")
    
    # Check Redis
    try:
        r = redis.Redis(host="localhost", port=6379)
        r.ping()
        checks["redis"] = True
    except Exception as e:
        logger.error(f"Redis check failed: {e}")
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks
    }
```

---

## 6. ALERTING SETUP

### CloudWatch Alarms (AWS)
```python
# infrastructure/alarms.tf

resource "aws_cloudwatch_metric_alarm" "api_error_rate" {
  alarm_name          = "api-error-rate-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "APIErrorRate"
  namespace           = "CustomMetrics"
  period              = "300"
  statistic           = "Average"
  threshold           = "5"
  alarm_description   = "Alert when API error rate exceeds 5%"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "db_connections" {
  alarm_name          = "db-connection-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Alert when DB connections exceed 80"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

---

## 7. BACKUP & DISASTER RECOVERY

### Automated Backups
```python
# backend/scripts/backup.py

import subprocess
from datetime import datetime
import boto3

def backup_database():
    """Backup PostgreSQL database to S3"""
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"backup_{timestamp}.sql.gz"
    
    # Dump database
    cmd = f"""
    PGPASSWORD={os.getenv('DB_PASSWORD')} pg_dump \
        --host {os.getenv('DB_HOST')} \
        --user {os.getenv('DB_USER')} \
        {os.getenv('DB_NAME')} | gzip > {backup_file}
    """
    
    subprocess.run(cmd, shell=True)
    
    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(
        backup_file,
        'my-backup-bucket',
        f'database/{backup_file}'
    )
    
    # Clean local file
    os.remove(backup_file)
    
    print(f"Backup completed: {backup_file}")

# Schedule with cron
# 0 2 * * * /usr/bin/python3 /app/backend/scripts/backup.py
```

### Restore from Backup
```bash
#!/bin/bash

BACKUP_FILE=$1

# Download from S3
aws s3 cp s3://my-backup-bucket/database/$BACKUP_FILE .

# Restore to database
PGPASSWORD=$DB_PASSWORD gunzip < $BACKUP_FILE | \
    psql --host $DB_HOST --user $DB_USER $DB_NAME

echo "Restore completed"
```

---

## 8. ENVIRONMENT CONFIGURATION

### Production Environment Variables
```bash
# .env.production

# Environment
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@rds-instance.aws.com/dropshipping
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40

# Cache
REDIS_HOST=redis.cache.amazonaws.com
REDIS_PORT=6379

# Security
SECRET_KEY=<generate-with-secrets.token_hex(32)>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Payments
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Email
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=SG.xxxxx

# Error Tracking
SENTRY_DSN=https://xxx@sentry.io/xxx

# Monitoring
DATADOG_API_KEY=xxx
DATADOG_SITE=datadoghq.com

# Web Scraping (optional)
PROXY_LIST=proxy1.com:8080,proxy2.com:8080
```

---

## 9. DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Security scan passed
- [ ] Database migrations tested
- [ ] Environment variables set
- [ ] Backups verified
- [ ] Monitoring configured
- [ ] Alarms configured

### Deployment
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Monitor logs for errors
- [ ] Deploy to production
- [ ] Run post-deployment tests
- [ ] Verify all endpoints
- [ ] Check monitoring dashboards

### Post-Deployment
- [ ] Monitor error rates
- [ ] Check database performance
- [ ] Verify backups
- [ ] Review logs
- [ ] Update status page

---

## 10. SCALING CONSIDERATIONS

### Horizontal Scaling (Multiple Instances)
- Load balancer distributes traffic
- Stateless API servers
- Shared database
- Shared Redis cache
- Kubernetes for orchestration

### Vertical Scaling (Larger Instances)
- Increase CPU/RAM on instances
- Database read replicas
- Database connection pooling
- Query optimization

### Database Optimization
```python
# Add indexes for common queries
from sqlalchemy import Index

class Product(Base):
    __tablename__ = "products"
    # ... columns ...
    
    __table_args__ = (
        Index('idx_tenant_created', 'tenant_id', 'created_at'),
        Index('idx_category_viability', 'category', 'viability_score'),
    )
```

---

## Quick Start Commands

```bash
# Local development
docker-compose up

# Run migrations
docker-compose exec backend alembic upgrade head

# Backup database
python backend/scripts/backup.py

# Run tests
pytest backend/tests

# Deploy to production
terraform apply
./scripts/deploy.sh

# View logs
tail -f /var/log/app.log | jq

# Scale backend to 5 instances
kubectl scale deployment backend --replicas=5
```
