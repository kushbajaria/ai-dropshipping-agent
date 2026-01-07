# Security & Compliance Guide

## 1. PAYMENT SECURITY (PCI DSS)

### DO NOT Store Credit Cards
- Never store raw credit card data
- Use Stripe's payment forms (Stripe.js)
- Use Stripe's hosted payment page (Stripe Checkout)
- Store only Stripe Customer ID and Payment Method ID

### Implementation Pattern
```python
# ✅ CORRECT: Use Stripe API
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Customer subscribes
customer = stripe.Customer.create(
    email=user_email,
    source=stripe_token  # Token from frontend
)

# Create subscription
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{"price": price_id}]
)

# ❌ WRONG: Never do this
def create_subscription_wrong(card_number, expiry, cvv):
    # This violates PCI DSS
    store_card_in_db(card_number, expiry, cvv)
```

### Payment Security Checklist
- [ ] Use Stripe/Razorpay tokenization
- [ ] Never log card numbers
- [ ] Enable 3D Secure
- [ ] Implement webhook verification
- [ ] Store webhook signatures
- [ ] Implement retry logic for failed payments
- [ ] Encrypt webhook secrets

---

## 2. DATA ENCRYPTION

### At Rest (Database)
```python
# Option 1: Database-level encryption (PostgreSQL)
# Enable pgcrypto extension
# CREATE EXTENSION pgcrypto;

# Option 2: Application-level encryption
from cryptography.fernet import Fernet
import os

CIPHER_KEY = os.getenv("CIPHER_KEY")  # Keep this in secrets manager
cipher_suite = Fernet(CIPHER_KEY)

def encrypt_sensitive_data(data: str) -> str:
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

# Usage in model
class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    key_encrypted = Column(String, nullable=False)  # Store encrypted
    
    @property
    def key_decrypted(self):
        return decrypt_sensitive_data(self.key_encrypted)
```

### In Transit (TLS)
```python
# Force HTTPS in FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

# Security headers
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

---

## 3. API KEY MANAGEMENT

### Secure API Key Storage
```python
import secrets
import hashlib
from datetime import datetime, timedelta

class APIKeyManager:
    
    @staticmethod
    def generate_key() -> str:
        """Generate a cryptographically secure API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_key(key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    @staticmethod
    def verify_key(provided_key: str, stored_hash: str) -> bool:
        """Verify provided key against stored hash"""
        return hashlib.sha256(provided_key.encode()).hexdigest() == stored_hash
    
    @staticmethod
    def create_api_key(tenant_id: int, name: str, db: Session) -> dict:
        """Create new API key"""
        key = APIKeyManager.generate_key()
        key_hash = APIKeyManager.hash_key(key)
        
        api_key = APIKey(
            tenant_id=tenant_id,
            key=key_hash,
            name=name,
            created_at=datetime.utcnow()
        )
        
        db.add(api_key)
        db.commit()
        
        # Return unhashed key ONLY once on creation
        return {
            "id": api_key.id,
            "key": key,  # Never return this again!
            "name": name
        }
    
    @staticmethod
    def rotate_key(key_id: int, db: Session) -> str:
        """Rotate an API key"""
        old_key = db.query(APIKey).filter(APIKey.id == key_id).first()
        
        new_key = APIKeyManager.generate_key()
        new_key_hash = APIKeyManager.hash_key(new_key)
        
        old_key.key = new_key_hash
        old_key.created_at = datetime.utcnow()
        db.commit()
        
        return new_key

# Usage in routes
@router.post("/api-keys")
def create_api_key(
    name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new API key for the tenant"""
    return APIKeyManager.create_api_key(
        tenant_id=current_user.tenant_id,
        name=name,
        db=db
    )

@router.post("/api-keys/{key_id}/rotate")
def rotate_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rotate an API key"""
    # Verify ownership
    key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.tenant_id == current_user.tenant_id
    ).first()
    
    if not key:
        raise HTTPException(status_code=404)
    
    new_key = APIKeyManager.rotate_key(key_id, db)
    return {"message": "API key rotated", "new_key": new_key}
```

---

## 4. INPUT VALIDATION & SQL INJECTION PREVENTION

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List

# Use Pydantic for input validation
class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    source: str = Field(..., regex="^[a-zA-Z0-9_-]+$")  # Whitelist pattern
    category: str = Field(..., min_length=1, max_length=100)
    cost_price: float = Field(..., gt=0, lt=1000000)
    
    @validator('title')
    def title_no_sql(cls, v):
        # Additional validation
        dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE']
        if any(keyword in v.upper() for keyword in dangerous_keywords):
            raise ValueError('Invalid title')
        return v

# SQLAlchemy automatically prevents SQL injection with parameterized queries
# ✅ CORRECT: SQLAlchemy parameterizes automatically
product = db.query(Product).filter(Product.title == user_input).first()

# ❌ WRONG: String concatenation
product = db.query(f"SELECT * FROM products WHERE title = '{user_input}'")
```

---

## 5. RATE LIMITING & DOS PROTECTION

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Per-endpoint rate limiting
@router.get("/products")
@limiter.limit("100/minute")
def get_products(request: Request, db: Session = Depends(get_db)):
    return db.query(Product).limit(100).all()

# Per-tenant rate limiting
@router.post("/products/analyze")
@limiter.limit("10/minute")
def analyze_products(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check quota
    if not await check_usage_quota(current_user.tenant_id, "/products/analyze"):
        raise HTTPException(
            status_code=429,
            detail="Monthly quota exceeded"
        )
    
    # ... process products ...
    log_usage(current_user.tenant_id)
```

---

## 6. AUDIT LOGGING

```python
from functools import wraps

def audit_log(action: str, resource_type: str):
    """Decorator for audit logging"""
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            result = await func(request, *args, **kwargs)
            
            # Log the action
            log = AuditLog(
                tenant_id=request.state.tenant_id,
                user_id=request.state.user_id,
                action=action,
                resource_type=resource_type,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent"),
                changes=kwargs
            )
            
            db = next(get_db())
            db.add(log)
            db.commit()
            db.close()
            
            return result
        return wrapper
    return decorator

# Usage
@router.post("/users")
@audit_log("created", "user")
async def create_user(user: UserCreate, current_user: User = Depends(get_current_user)):
    # ... create user ...
    pass
```

---

## 7. WEB SCRAPING COMPLIANCE

### Robots.txt Checker
```python
import aiohttp
from urllib.robotparser import RobotFileParser

class ScrapingCompliance:
    
    @staticmethod
    async def check_robots_txt(url: str, user_agent: str = "AIDropshipBot") -> bool:
        """Check if scraping is allowed by robots.txt"""
        try:
            rp = RobotFileParser()
            rp.set_user_agent(user_agent)
            rp.read_file(f"{url}/robots.txt")
            return rp.can_fetch(user_agent, url)
        except Exception as e:
            print(f"Error checking robots.txt: {e}")
            return False
    
    @staticmethod
    async def scrape_with_backoff(
        url: str,
        max_retries: int = 3,
        base_delay: int = 1
    ):
        """Scrape with exponential backoff"""
        import asyncio
        
        async with aiohttp.ClientSession() as session:
            for attempt in range(max_retries):
                try:
                    # Add proper User-Agent
                    headers = {
                        'User-Agent': 'AIDropshipBot/1.0 (+https://yourdomain.com/bot)'
                    }
                    
                    async with session.get(url, headers=headers, timeout=10) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        elif resp.status == 429:
                            # Rate limited - back off
                            wait_time = base_delay ** attempt
                            await asyncio.sleep(wait_time)
                        elif resp.status == 403:
                            # Forbidden - stop trying
                            raise Exception("Access denied by website")
                except Exception as e:
                    print(f"Scrape attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(base_delay ** attempt)
        
        raise Exception("Failed to scrape after max retries")
```

### ToS Compliance
```python
SCRAPING_POLICIES = {
    "amazon.com": {
        "allowed": False,
        "reason": "Violates ToS - use Product Advertising API instead"
    },
    "aliexpress.com": {
        "allowed": True,
        "min_delay_seconds": 2,
        "rate_limit": "100/hour"
    },
    "ebay.com": {
        "allowed": True,
        "min_delay_seconds": 1,
        "rate_limit": "500/hour"
    }
}

def is_scraping_allowed(domain: str) -> tuple[bool, str]:
    """Check if scraping is allowed for domain"""
    policy = SCRAPING_POLICIES.get(domain)
    if not policy:
        return False, "Domain not in approved list"
    
    return policy.get("allowed", False), policy.get("reason", "")
```

---

## 8. GDPR COMPLIANCE

```python
from datetime import datetime, timedelta

class GDPRManager:
    
    @staticmethod
    def export_user_data(user_id: int, db: Session) -> dict:
        """Export all user data (Right to Data Portability)"""
        user = db.query(User).filter(User.id == user_id).first()
        
        return {
            "user": {
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "is_active": user.is_active
            },
            "products": [
                {
                    "title": p.title,
                    "created_at": p.created_at.isoformat()
                }
                for p in db.query(Product).filter(Product.tenant_id == user.tenant_id).all()
            ],
            "usage": [
                {
                    "endpoint": u.endpoint,
                    "created_at": u.created_at.isoformat()
                }
                for u in db.query(ApiUsage).filter(ApiUsage.tenant_id == user.tenant_id).all()
            ]
        }
    
    @staticmethod
    def delete_user_data(user_id: int, db: Session):
        """Delete all user data (Right to be forgotten)"""
        user = db.query(User).filter(User.id == user_id).first()
        tenant_id = user.tenant_id
        
        # Soft delete - mark as deleted instead of removing
        user.email = f"deleted_{user_id}_{datetime.utcnow().timestamp()}"
        user.is_active = False
        
        # Anonymize products
        products = db.query(Product).filter(Product.tenant_id == tenant_id).all()
        for product in products:
            product.title = "DELETED"
            product.ai_summary = None
        
        db.commit()
    
    @staticmethod
    def cleanup_old_data(days_old: int = 30, db: Session = None):
        """Delete data older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Delete old usage logs
        db.query(ApiUsage).filter(ApiUsage.created_at < cutoff_date).delete()
        
        db.commit()
```

---

## 9. SECURITY HEADERS

```python
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent XSS
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # HTTPS enforcement
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
        
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

---

## Compliance Checklist

### Before Launch
- [ ] Implement JWT authentication
- [ ] Enable HTTPS everywhere
- [ ] Set up rate limiting
- [ ] Add input validation
- [ ] Implement audit logging
- [ ] Add security headers
- [ ] Encrypt sensitive data
- [ ] Secure API key storage
- [ ] Payment security (use Stripe tokens)
- [ ] GDPR data export/deletion endpoints
- [ ] Privacy Policy published
- [ ] Terms of Service published
- [ ] Data Processing Agreement ready
- [ ] Security audit completed
- [ ] Penetration testing done

### Ongoing
- [ ] Monitor for security vulnerabilities
- [ ] Regular security updates
- [ ] Weekly backup testing
- [ ] Monthly audit log review
- [ ] Quarterly penetration testing
- [ ] Annual security audit
