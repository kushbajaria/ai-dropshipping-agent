# SAAS Platform - Quick Reference Card

Print this and put it on your desk while building! 

---

## 🚨 The Golden Rules (NEVER BREAK THESE)

```
1. NEVER store credit card numbers
   → Use Stripe tokens only

2. NEVER store passwords in plaintext
   → Hash with bcrypt

3. NEVER mix tenant data in queries
   → Always filter by tenant_id

4. NEVER send passwords over HTTP
   → Use HTTPS everywhere

5. NEVER log passwords/tokens
   → Only log actions and IDs

6. NEVER trust user input directly
   → Validate and sanitize everything

7. NEVER run a single instance in production
   → Use load balancing

8. NEVER skip backups
   → Test restoration daily

9. NEVER deploy without monitoring
   → Set up Sentry before launch

10. NEVER ignore security warnings
    → Fix them immediately
```

---

## 📋 Authentication Checklist

### Registration
- [ ] Email validation
- [ ] Password strength (min 12 chars)
- [ ] Password hashed with bcrypt
- [ ] Tenant created
- [ ] User created in tenant
- [ ] Verification email sent
- [ ] Rate limit on signup attempts

### Login
- [ ] Email exists check
- [ ] Password verification
- [ ] Account active check
- [ ] Tenant active check
- [ ] JWT access token issued
- [ ] Refresh token issued
- [ ] Login attempt logged
- [ ] Rate limit on failed attempts

### Token Handling
- [ ] Access token expires (30 min)
- [ ] Refresh token expires (7 days)
- [ ] Token rotation on refresh
- [ ] Invalid token returns 401
- [ ] Expired token returns 401
- [ ] Token stored securely (httponly cookie or secure storage)

---

## 🛡️ Security Checklist (Per Endpoint)

For EVERY endpoint you create, ask:

- [ ] Is it HTTPS only?
- [ ] Does it require authentication?
- [ ] Does it check tenant isolation?
- [ ] Does it validate input?
- [ ] Does it have rate limiting?
- [ ] Does it log the action?
- [ ] Does it return sanitized output?
- [ ] Is there proper error handling?
- [ ] Are there security headers?
- [ ] Is SQL injection prevented?

---

## 💳 Payment Processing Checklist

### Stripe Setup
- [ ] Create Stripe account
- [ ] Get API keys (test mode first)
- [ ] Add API keys to environment
- [ ] Install stripe library
- [ ] Create webhook endpoint
- [ ] Verify webhook signature
- [ ] Test in Stripe dashboard

### Subscription Creation
- [ ] Collect card on frontend with Stripe.js
- [ ] Receive token (not card number)
- [ ] Create Stripe customer with token
- [ ] Store customer_id in DB
- [ ] Create subscription in Stripe
- [ ] Update subscription status in DB
- [ ] Send confirmation email

### Ongoing Billing
- [ ] Listen for payment_intent.succeeded
- [ ] Listen for customer.subscription.updated
- [ ] Listen for invoice.payment_failed
- [ ] Update subscription status
- [ ] Create invoice record
- [ ] Retry failed payments
- [ ] Notify user of failures

---

## 📊 Multi-Tenancy Checklist

### Data Model
- [ ] All tables have tenant_id
- [ ] tenant_id is indexed
- [ ] Foreign key to tenants table
- [ ] Combined index (tenant_id, other_column)

### Queries
- [ ] All queries filter by tenant_id
- [ ] No cross-tenant data access
- [ ] No global data leakage
- [ ] Admin queries scope correctly

### API
- [ ] Tenant extracted from JWT
- [ ] Tenant passed to all queries
- [ ] 403 Forbidden if tenant mismatch
- [ ] Never expose other tenant's data

### Testing
- [ ] User A can't see User B's data
- [ ] User A can't modify User B's data
- [ ] User A can't delete User B's data
- [ ] Admin sees all correct tenants

---

## ⚡ Rate Limiting Levels

### Endpoint Level (Slowapi)
```python
@limiter.limit("100/minute")
def get_products():
    pass

Common limits:
- Read endpoints: 100/minute
- Write endpoints: 10/minute
- Auth endpoints: 5/minute
- Admin endpoints: 1000/minute
```

### User Level (Redis)
```
FREE tier: 100 requests/month
PRO tier: 10,000 requests/month
ENTERPRISE: unlimited

Track with: user_quota_{user_id}
```

### Global Level (DDoS)
```
Use CloudFlare for automatic DDoS protection
Configure WAF rules
Enable rate limiting at edge
```

---

## 📝 Logging What to Track

### Track These (Security)
```
✅ Login attempts (success/fail)
✅ Signup new user
✅ Password changes
✅ Permission changes
✅ API key creation
✅ API key rotation
✅ Subscription changes
✅ Failed payment attempts
✅ Data exports
✅ Data deletions
```

### DON'T Track These (Security)
```
❌ Passwords (plaintext or hashed)
❌ API keys (full)
❌ Credit card numbers
❌ Tokens (full)
❌ Personal info (SSN, passport)
```

### Format These
```json
{
  "timestamp": "2024-01-06T12:34:56Z",
  "event": "user_login",
  "user_id": 123,
  "tenant_id": 45,
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "result": "success",
  "resource": "user:123",
  "changes": null
}
```

---

## 🚀 Before You Deploy

### Week Before
- [ ] Code review complete
- [ ] Security audit done
- [ ] Load testing passed
- [ ] Database backed up
- [ ] Monitoring configured
- [ ] Alerts configured
- [ ] On-call rotation set up

### Day Before
- [ ] Staging deployment tested
- [ ] Database migration tested
- [ ] Backups verified
- [ ] Rollback plan documented
- [ ] Status page updated
- [ ] Team on standby

### Deployment Day
- [ ] 2 people present
- [ ] Deployment script ready
- [ ] Monitoring dashboard open
- [ ] Status page open
- [ ] Communication channel active
- [ ] Coffee ready ☕

### Post Deployment
- [ ] Check error rates (should be 0%)
- [ ] Check performance (p95 < 200ms)
- [ ] Spot check features working
- [ ] Read logs for warnings
- [ ] Check DB performance
- [ ] Monitor for 2 hours
- [ ] Update team on Slack
- [ ] Go on vacation (kidding... but you earned it!)

---

## 💰 Pricing Strategy Template

```
FREE
├─ $0/month
├─ 100 API calls/month
├─ 1 user
├─ Community support
└─ Great for trying it out

PRO
├─ $29/month
├─ 10,000 API calls/month
├─ 5 users
├─ Email support
└─ Perfect for growing teams

ENTERPRISE
├─ Custom pricing
├─ Unlimited everything
├─ Dedicated account manager
├─ Phone support
└─ For large organizations
```

---

## 🏗️ Directory Structure

```
ai-dropshipping-agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── database.py      # DB connection
│   │   ├── security.py      # JWT & bcrypt
│   │   ├── config.py        # Settings
│   │   ├── models/          # Database models
│   │   │   ├── __init__.py
│   │   │   ├── tenant.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── subscription.py
│   │   │   └── api_key.py
│   │   ├── routes/          # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   ├── subscriptions.py
│   │   │   └── health.py
│   │   ├── schemas/         # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   └── product.py
│   │   └── middleware/      # Custom middleware
│   │       ├── __init__.py
│   │       ├── audit_log.py
│   │       ├── error_handling.py
│   │       └── security_headers.py
│   ├── migrations/          # Alembic migrations
│   ├── tests/               # Unit tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── SAAS_ARCHITECTURE.md
│   ├── IMPLEMENTATION_GUIDE.md
│   ├── SECURITY_COMPLIANCE.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── QUICKSTART.md
└── docker-compose.yml
```

---

## 🧪 Quick Test Commands

```bash
# Test signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","company_name":"Test","full_name":"John"}'

# Test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Test with JWT token
curl -X GET http://localhost:8000/products \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Test rate limiting
for i in {1..101}; do
  curl http://localhost:8000/products \
    -H "Authorization: Bearer TOKEN" 2>&1 | grep -q "429" && echo "Rate limited at request $i"
done
```

---

## 📞 Emergency Numbers

### If Production is Down
```
1. Check monitoring (Sentry/CloudWatch)
   → See error logs

2. Check database
   → Is PostgreSQL responding?
   → Are connections healthy?

3. Check infrastructure
   → ALB health
   → EC2 instance status
   → Network connectivity

4. Check recent deployments
   → Was something deployed recently?
   → Rollback if needed

5. Notify customers
   → Update status page
   → Send email notification
```

### If Payment Processing Fails
```
1. Check Stripe dashboard
   → Are webhooks being received?
   → Are there payment failures?

2. Check webhook logs
   → Are webhooks being processed?
   → Are there errors?

3. Retry mechanism
   → Run manual retry job
   → Update subscription status

4. Contact Stripe support
   → Check API status page
```

---

## 📚 Quick Links

| Topic | File | Section |
|-------|------|---------|
| Architecture | SAAS_ARCHITECTURE.md | All |
| Getting Started | QUICKSTART.md | All |
| Code Templates | IMPLEMENTATION_GUIDE.md | Sections 1-4 |
| Security Checklists | SECURITY_COMPLIANCE.md | Section 10 |
| Going Live | DEPLOYMENT_GUIDE.md | Section 9 |
| What Changed | TRANSFORMATION_GUIDE.md | All |

---

## ✅ Done! What's Next?

1. **Right Now**: Read QUICKSTART.md
2. **Today**: Set up PostgreSQL locally
3. **This Week**: Implement authentication
4. **Next Week**: Add multi-tenancy
5. **Week 3**: Integrate Stripe
6. **Week 4+**: Ship to production!

---

**You've got this! 🚀**
