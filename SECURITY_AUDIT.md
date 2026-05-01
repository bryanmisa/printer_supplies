# SuppliesPro - Security Audit Report

Generated: 2026-05-01
Project: SuppliesPro Printer Inventory Management

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| HIGH     | 2     | Need Fix |
| MEDIUM   | 3     | Need Fix |
| LOW      | 2     | Review |

## HIGH Severity Issues

### 1. SECRET_KEY Exposure
**File:** `printer_supplies/settings.py:7`
**Issue:** Default secret key is hardcoded and insecure
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
```
**Risk:** 
- Session hijacking
- CSRF token prediction
- Cryptographic weakness

**Fix Required:**
Create `.env` file with a strong secret key:
```bash
python -c "import secrets; print(secrets.token_hex(50))"
```
Add to `.env`:
```
SECRET_KEY=your-generated-secret-key-here
```

---

### 2. DEBUG Mode Enabled
**File:** `printer_supplies/settings.py:9`
**Issue:** DEBUG=True in production exposes:
- Stack traces
- Database queries
- Environment variables
- Source code snippets

**Fix Required:**
Ensure `.env` contains:
```
DEBUG=False
```

---

## MEDIUM Severity Issues

### 3. ALLOWED_HOSTS Too Permissive
**File:** `printer_supplies/settings.py:11` (development)
**Issue:** `ALLOWED_HOSTS = ['*']` allows Host header attacks

**Fix Required:**
In `.env`:
```
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

In production (`dist/SuppliesPro/app/printer_supplies/settings.py:11`):
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
```
Already fixed in production settings.

---

### 4. Outdated Package: reportlab
**Issue:** reportlab 4.4.10 has known vulnerabilities (CVE-2023-33733)
**Current:** 4.4.10
**Latest:** 4.5.0

**Fix:**
```bash
pip install --upgrade reportlab
```

---

### 5. Missing Security Headers
**Issue:** Some security middleware is present but missing HSTS and referrer policy.

**Current Middleware (settings.py:25-35):**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Present
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'rbac.middleware.RBACMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Recommended Additions to settings.py:**
```python
# Security headers (add after MIDDLEWARE)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

---

## LOW Severity Issues

### 6. Session Cookie Age
**File:** `settings.py:95`
**Issue:** SESSION_COOKIE_AGE = 3600 (1 hour) may be too short for convenience

**Recommendation:** Adjust based on your needs (e.g., 86400 for 24 hours)

---

### 7. Weak Password Validators
**File:** `settings.py:66-71`
**Issue:** Default Django password validators may be too lenient

**Current:**
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

**Recommendation:** Add minimum length requirement:
```python
{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
```

---

## Checklist for Production Deployment

- [ ] Generate strong SECRET_KEY and add to `.env`
- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `ALLOWED_HOSTS` with specific domains
- [ ] Upgrade `reportlab` to 4.5.0+
- [ ] Add security headers to settings.py
- [ ] Review session cookie age
- [ ] Strengthen password validators
- [ ] Ensure `.env` is in `.gitignore` (not committed)
- [ ] Use HTTPS in production (configure SSL certificate)
- [ ] Set up firewall rules (only allow ports 80, 443, 22)
- [ ] Regularly update dependencies: `pip list --outdated`

---

## Files to Update

1. `printer_supplies/settings.py` - Add security settings
2. `.env` - Create with secure values (don't commit!)
3. `.env.example` - Update with new variables
4. `requirements.txt` - Update reportlab version

---

## Quick Security Fix Script

Run this to fix common issues:

```bash
# Generate secure secret key
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(50))')" >> .env

# Set debug to false
echo "DEBUG=False" >> .env

# Set allowed hosts
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env

# Upgrade reportlab
pip install --upgrade reportlab

# Add to .gitignore
echo ".env" >> .gitignore
```

---

## Notes

- The `dist/SuppliesPro/app/printer_supplies/settings.py` already has better `ALLOWED_HOSTS` default
- WhiteNoise middleware is properly configured for static file serving
- CSRF middleware is enabled
- X-Frame-Options is enabled (clickjacking protection)
- RBAC middleware provides additional access control
