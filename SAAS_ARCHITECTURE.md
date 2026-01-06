# SAAS Platform Architecture Guide: AI Dropshipping Agent

## Overview
This document outlines the complete architecture needed to build a secure, scalable SAAS platform for AI-powered product discovery in dropshipping.

---

## 1. CORE SAAS REQUIREMENTS

### 1.1 Multi-Tenancy
- **Current Status**: ⚠️ Needs implementation
- **What's needed**: 
  - Isolate data per tenant (User)
  - Tenant context in all queries
  - Row-level security policies
  - Separate API keys per user

### 1.2 Subscription Management
- **Current Status**: ❌ Not implemented
- **What's needed**:
  - Subscription tiers (Free, Pro, Enterprise)
  - Usage quotas per tier
  - Subscription status tracking
  - Billing cycle management

### 1.3 Payment Processing
- **Current Status**: ❌ Not implemented
- **What's needed**:
  - Stripe/Razorpay integration
  - PCI DSS compliance
  - Webhook handling for payment events
  - Invoice generation
  - Refund handling

---

## 2. SECURITY ARCHITECTURE

### 2.1 Authentication & Authorization
- **Current Status**: ⚠️ Basic API key auth only
- **Improvements needed**:
  - JWT tokens with refresh tokens
  - Password hashing (bcrypt)
  - MFA support
  - Session management
  - Role-based access control (RBAC)

### 2.2 Data Protection
- **Current Status**: ⚠️ Partial
- **What's needed**:
  - Encryption at rest (database)
  - Encryption in transit (TLS)
  - API key rotation
  - Secure password storage (bcrypt with salt)
  - Data masking for PII

### 2.3 API Security
- **Current Status**: ⚠️ Basic
- **What's needed**:
  - Rate limiting per user/tenant
  - Request validation & sanitization
  - CORS configuration
  - Input validation & SQL injection prevention
  - Request signing for webhooks
  - HTTPS enforcement

### 2.4 Web Scraping Compliance
- **Critical Legal Considerations**:
  - Respect robots.txt
  - Add delays between requests
  - Identify user agent properly
  - Comply with platform ToS
  - Handle 429/403 responses gracefully
  - Monitor for IP bans

---

## 3. DATABASE ARCHITECTURE

### 3.1 Production Database
- **Current**: SQLite (development only)
- **Production**: PostgreSQL recommended
- **Why**: ACID compliance, concurrent users, JSON fields, better scaling

### 3.2 Data Schema Improvements
- Add tenant isolation column to all tables
- Add soft deletes (deleted_at timestamp)
- Add audit logs (created_by, updated_by, updated_at)
- Indexes on frequently queried fields
- Partitioning strategy for large tables

### 3.3 Data Retention & Privacy
- GDPR right to be forgotten implementation
- Data expiration policies
- Backup & recovery procedures
- Data residency compliance

---

## 4. BILLING & USAGE TRACKING

### 4.1 Usage Metrics
- API calls per month
- Products analyzed per month
- Storage usage
- Custom metrics per tier

### 4.2 Subscription Tiers
```
FREE:
  - 100 API calls/month
  - 1 user per account
  - Limited to 1 category search

PRO:
  - 10,000 API calls/month
  - 5 users per account
  - Unlimited category searches
  - Email support

ENTERPRISE:
  - Unlimited API calls
  - Unlimited users
  - Priority support
  - Custom integrations
```

### 4.3 Metering & Invoicing
- Real-time usage tracking
- Overage pricing
- Automated invoicing
- Payment retry logic

---

## 5. OPERATIONS & MONITORING

### 5.1 Logging & Monitoring
- Structured logging (JSON format)
- Error tracking (Sentry recommended)
- Performance monitoring
- User activity logs
- API request/response logging

### 5.2 Alerting
- Failed payment alerts
- API error rate alerts
- Scraping failure alerts
- Quota exceeded alerts

### 5.3 Performance
- Database query optimization
- API response time targets (<200ms)
- Caching strategy (Redis)
- Rate limiting implementation

---

## 6. LEGAL & COMPLIANCE

### 6.1 Terms & Conditions
- Define acceptable use
- Scraping restrictions
- Data ownership clarification
- Liability limitations
- Refund policy

### 6.2 Privacy Policy
- Data collection practices
- Data storage & retention
- User rights
- GDPR compliance
- CCPA compliance (if applicable)

### 6.3 Compliance Checklist
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Web Scraping ToS compliance
- [ ] GDPR compliance
- [ ] Data processing agreement
- [ ] Security audit
- [ ] Penetration testing
- [ ] PCI DSS compliance (if storing cards)

---

## 7. TECHNICAL STACK RECOMMENDATIONS

### Backend
- FastAPI ✅ (already using)
- PostgreSQL (production DB)
- Redis (caching & rate limiting)
- Celery (async job queue for scraping)
- Stripe API (payments)

### Infrastructure
- Docker containers
- Kubernetes or managed services (AWS ECS, Railway, Render)
- SSL/TLS certificates
- CDN for static assets
- WAF (Web Application Firewall)

### Monitoring & Analytics
- Sentry (error tracking)
- DataDog/New Relic (APM)
- CloudWatch/ELK (logging)
- Prometheus (metrics)

---

## 8. IMPLEMENTATION PRIORITY

### Phase 1 (Critical - Week 1-2)
1. User registration & login system
2. JWT authentication
3. Multi-tenancy data isolation
4. Basic subscription tracking
5. Rate limiting
6. HTTPS enforcement

### Phase 2 (High - Week 3-4)
1. Payment gateway integration
2. Subscription management
3. Usage tracking & quotas
4. Admin dashboard
5. Audit logging

### Phase 3 (Medium - Week 5-6)
1. Advanced monitoring
2. MFA support
3. API key management UI
4. Automated billing
5. Invoice generation

### Phase 4 (Polish)
1. Performance optimization
2. Security hardening
3. Compliance documentation
4. Disaster recovery setup

---

## 9. CURRENT GAPS & ACTION ITEMS

| Component | Status | Priority | Effort |
|-----------|--------|----------|--------|
| User registration | ❌ | P0 | 2 days |
| JWT auth | ❌ | P0 | 1 day |
| Multi-tenancy | ⚠️ | P0 | 3 days |
| Payment integration | ❌ | P1 | 3 days |
| Rate limiting | ⚠️ | P1 | 1 day |
| Usage tracking | ⚠️ | P1 | 2 days |
| Admin dashboard | ❌ | P2 | 5 days |
| Monitoring/Logging | ⚠️ | P2 | 3 days |
| Legal docs | ❌ | P1 | 2 days |

---

## 10. SECURITY CHECKLIST

### Authentication
- [ ] Password hashing with bcrypt
- [ ] JWT with expiration
- [ ] Refresh token rotation
- [ ] Secure session management
- [ ] MFA support

### API Security
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS protection

### Data Security
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] API key rotation mechanism
- [ ] Audit logging
- [ ] Data masking for PII

### Infrastructure
- [ ] Secrets management (AWS Secrets Manager, HashiCorp Vault)
- [ ] WAF enabled
- [ ] DDoS protection
- [ ] Regular backups with testing
- [ ] Security group rules

### Compliance
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Data Processing Agreement
- [ ] Incident response plan
- [ ] Penetration testing done

---

## 11. WEB SCRAPING BEST PRACTICES

### Ethical Scraping
1. **Respect robots.txt** - Always check and follow
2. **Add delays** - Minimum 1-2 seconds between requests
3. **User-Agent** - Identify your bot properly
4. **Rate limit** - Don't overwhelm servers
5. **Cache results** - Avoid redundant requests

### Error Handling
- Handle 429 (Too Many Requests) with exponential backoff
- Handle 403 (Forbidden) gracefully
- Implement IP rotation if needed
- Log blocked requests

### Legal
- Include scraping clause in ToS
- Get explicit consent from users
- Don't scrape protected data
- Comply with CFAA (Computer Fraud and Abuse Act)
- Check platform's ToS before scraping

---

## Next Steps
1. Review the IMPLEMENTATION_GUIDE.md for step-by-step setup
2. Start with Phase 1 components
3. Set up development environment with PostgreSQL
4. Implement authentication system
5. Add multi-tenancy to existing models
