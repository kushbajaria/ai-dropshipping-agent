# Phase 1 Implementation Guide

This guide walks you through implementing the critical SAAS components for production readiness.

## 1. Enhanced Database Models with Multi-Tenancy

Create `backend/app/models/enhanced_models.py`:

```python
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    subscription_tier = Column(String(50), default="free")  # free, pro, enterprise
    subscription_status = Column(String(50), default="active")  # active, paused, cancelled
    stripe_customer_id = Column(String(255), unique=True)
    api_quota_monthly = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="tenant", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    usage = relationship("ApiUsage", back_populates="tenant", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    
    __table_args__ = (
        # Unique constraint on email per tenant
        UniqueConstraint('tenant_id', 'email', name='uq_tenant_user_email'),
    )

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    last_used = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="api_keys")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    category = Column(String, nullable=False)
    
    cost_price = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=False)
    shipping_time_days = Column(Integer, nullable=False)
    
    selling_price = Column(Float, nullable=False)
    rating = Column(Float)
    review_count = Column(Integer)
    
    demand_score = Column(Float)
    competition_score = Column(Float)
    risk_score = Column(Float)
    viability_score = Column(Float)
    
    ai_summary = Column(Text)
    metadata = Column(JSON)  # Store any additional data
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="products")

class ApiUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    api_key = Column(String, index=True, nullable=False)
    endpoint = Column(String, nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, etc
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="usage")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)  # created, updated, deleted, login_failed, etc
    resource_type = Column(String(100), nullable=False)  # user, product, api_key, etc
    resource_id = Column(Integer)
    changes = Column(JSON)  # What changed
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
```

## 2. JWT Authentication System

Create `backend/app/security.py`:

```python
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt
from passlib.context import CryptContext
import os
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(credentials: HTTPAuthCredentials, db: Session = Depends(get_db)):
    """Verify JWT token and return user"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        tenant_id: int = payload.get("tenant_id")
        
        if user_id is None or tenant_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id,
        User.is_active == True
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {"user": user, "tenant_id": tenant_id}

async def get_current_user(
    credentials: Annotated[HTTPAuthCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Dependency to get current authenticated user"""
    result = await verify_token(credentials, db)
    return result["user"]

async def get_current_tenant(
    credentials: Annotated[HTTPAuthCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
) -> int:
    """Dependency to get current tenant ID"""
    result = await verify_token(credentials, db)
    return result["tenant_id"]
```

## 3. Rate Limiting Middleware

Create `backend/app/rate_limit.py`:

```python
from fastapi import Request, HTTPException, status
from functools import wraps
from datetime import datetime, timedelta
import redis
import os
from typing import Optional

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 3600,
    key_func=None
):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Get identifier (IP, API key, or user ID)
            if key_func:
                identifier = key_func(request)
            else:
                identifier = request.client.host
            
            # Create rate limit key
            rate_key = f"rate_limit:{identifier}:{func.__name__}"
            
            try:
                # Try to get current count
                current = redis_client.incr(rate_key)
                
                # Set expiry on first request
                if current == 1:
                    redis_client.expire(rate_key, window_seconds)
                
                # Check if exceeded
                if current > max_requests:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded"
                    )
            except redis.ConnectionError:
                # If Redis fails, allow request but log it
                print(f"Redis connection error for rate limiting")
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

async def check_usage_quota(tenant_id: int, endpoint: str) -> bool:
    """Check if tenant has exceeded monthly quota"""
    current_date = datetime.now()
    month_key = f"usage:{tenant_id}:{current_date.year}:{current_date.month}"
    
    try:
        usage = redis_client.get(month_key) or 0
        quota_key = f"quota:{tenant_id}"
        quota = redis_client.get(quota_key)
        
        if quota and int(usage) >= int(quota):
            return False
    except redis.ConnectionError:
        pass
    
    return True

def log_usage(tenant_id: int):
    """Log API usage for quota tracking"""
    current_date = datetime.now()
    month_key = f"usage:{tenant_id}:{current_date.year}:{current_date.month}"
    
    try:
        redis_client.incr(month_key)
        # Set expiry to 35 days (covers month boundaries)
        redis_client.expire(month_key, 35 * 24 * 60 * 60)
    except redis.ConnectionError:
        pass
```

## 4. Authentication Routes

Create `backend/app/routes/auth.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    full_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """Register a new tenant and user"""
    
    # Check if tenant already exists
    existing_tenant = db.query(Tenant).filter(Tenant.email == request.email).first()
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create tenant
    tenant = Tenant(
        name=request.company_name,
        email=request.email
    )
    db.add(tenant)
    db.flush()  # Get tenant ID without committing
    
    # Create user
    user = User(
        tenant_id=tenant.id,
        email=request.email,
        hashed_password=hash_password(request.password),
        full_name=request.full_name,
        is_admin=True  # First user is admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.refresh(tenant)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.id, "tenant_id": tenant.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "tenant_id": tenant.id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with email and password"""
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.id, "tenant_id": user.tenant_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "tenant_id": user.tenant_id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "tenant_id": current_user.tenant_id,
        "is_admin": current_user.is_admin
    }
```

## 5. Subscription Tiers Configuration

Create `backend/app/config/subscriptions.py`:

```python
from enum import Enum

class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

SUBSCRIPTION_CONFIG = {
    "free": {
        "name": "Free",
        "price_monthly": 0,
        "api_calls_per_month": 100,
        "max_users": 1,
        "features": [
            "Basic product analysis",
            "Community support"
        ]
    },
    "pro": {
        "name": "Pro",
        "price_monthly": 2999,  # $29.99
        "api_calls_per_month": 10000,
        "max_users": 5,
        "features": [
            "Advanced analytics",
            "Multiple category searches",
            "Email support",
            "API access"
        ]
    },
    "enterprise": {
        "name": "Enterprise",
        "price_monthly": "custom",
        "api_calls_per_month": "unlimited",
        "max_users": "unlimited",
        "features": [
            "Unlimited everything",
            "Priority support",
            "Custom integration",
            "SLA guarantee"
        ]
    }
}
```

## 6. Environment Variables Template

Create `backend/.env.example`:

```
# Database
DATABASE_URL=postgresql://user:password@localhost/ai_dropshipping

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
SECRET_KEY=your-super-secret-key-change-in-production

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Environment
ENVIRONMENT=development
```

---

## Next Steps

1. Set up PostgreSQL locally
2. Update `database.py` to use PostgreSQL connection string
3. Implement the models, security, and auth routes
4. Test signup/login flow
5. Add rate limiting to product routes
6. Create admin dashboard for subscription management
