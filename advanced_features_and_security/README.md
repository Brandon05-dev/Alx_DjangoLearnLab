# 🔒 Advanced Features & Security - Django Library Management System

A comprehensive Django application demonstrating advanced security features, custom user models, permissions management, and security best practices.

## 📋 Table of Contents

- [Features](#features)
- [Security Implementations](#security-implementations)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Security Configurations](#security-configurations)
- [User Management](#user-management)
- [Permissions & Groups](#permissions--groups)
- [HTTPS & SSL Setup](#https--ssl-setup)
- [Deployment Guide](#deployment-guide)
- [Security Testing](#security-testing)
- [Contributing](#contributing)

## ✨ Features

### 🔐 Custom User Model
- **Extended User Fields**: Added `date_of_birth` and `profile_photo` fields
- **Custom User Manager**: Implements secure user creation with proper password hashing
- **Admin Integration**: Custom admin interface with enhanced user management

### 📚 Book Management
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Custom Permissions**: Fine-grained access control with `can_view`, `can_create`, `can_edit`, `can_delete`
- **Input Validation**: Comprehensive server-side validation and sanitization
- **Audit Trail**: Tracks who created/modified books and when

### 🛡️ Security Features
- **CSRF Protection**: All forms protected against Cross-Site Request Forgery
- **XSS Prevention**: Output escaping and Content Security Policy
- **SQL Injection Prevention**: Django ORM usage with parameterized queries
- **Permission-Based Access**: Role-based access control system
- **Secure Headers**: Comprehensive security headers implementation
- **HTTPS Enforcement**: SSL/TLS configuration for production

## 🔒 Security Implementations

### 1. Custom User Model & Authentication

```python
# models.py - CustomUser with additional security fields
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    objects = CustomUserManager()
```

**Security Benefits:**
- Centralized user management
- Additional verification fields
- Secure password handling through custom manager
- Profile photo upload with validation

### 2. Fine-Grained Permissions

```python
# models.py - Book model with custom permissions
class Meta:
    permissions = [
        ('can_view', 'Can view books'),
        ('can_create', 'Can create books'),
        ('can_edit', 'Can edit books'),
        ('can_delete', 'Can delete books'),
    ]
```

**Implementation:**
- **Groups**: Create `Viewers`, `Editors`, `Admins` groups in Django admin
- **Assignment**: Assign permissions to groups based on user roles
- **View Protection**: All views protected with `@permission_required` decorators

### 3. CSRF Protection

```python
# views.py - CSRF protection on all forms
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_book(request, book_id):
    # View implementation
```

```html
<!-- Templates - CSRF tokens in all forms -->
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### 4. Security Headers

```python
# settings.py - Comprehensive security headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

### 5. Content Security Policy

```python
# settings.py - Strict CSP configuration
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_OBJECT_SRC = ("'none'",)
```

## 📁 Project Structure

```
advanced_features_and_security/
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                         # This documentation
│
├── LibraryProject/                   # Main project configuration
│   ├── __init__.py
│   ├── settings.py                   # Security-hardened settings
│   ├── urls.py                       # URL routing
│   ├── wsgi.py                       # WSGI configuration
│   └── asgi.py                       # ASGI configuration
│
├── bookshelf/                        # Main application
│   ├── models.py                     # CustomUser & Book models
│   ├── views.py                      # Permission-protected views
│   ├── admin.py                      # Enhanced admin interface
│   ├── urls.py                       # Application URLs
│   ├── apps.py                       # App configuration
│   └── templates/bookshelf/          # Secure templates
│       ├── base.html                 # Base template with security headers
│       ├── home.html                 # Dashboard with permission display
│       ├── book_list.html            # Book listing with CSRF protection
│       ├── form_example.html         # Secure form example
│       └── login.html                # Secure login form
│
├── static/                           # Static files
├── media/                           # User uploads (profile photos)
└── logs/                            # Security and application logs
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### 1. Clone & Setup Environment

```bash
# Clone the repository
cd advanced_features_and_security

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Requirements File

```bash
# Create requirements.txt
cat > requirements.txt << EOF
Django>=4.2.0
django-csp>=3.7
Pillow>=9.0.0  # For ImageField support
EOF

pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations bookshelf
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Static Files & Media

```bash
# Create directories
mkdir -p static media/profile_photos logs

# Collect static files (for production)
python manage.py collectstatic
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## ⚙️ Security Configurations

### settings.py Security Settings Explained

#### 1. Debug & Secret Key
```python
# CRITICAL: Set to False in production
DEBUG = False

# CRITICAL: Use environment variable in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
```

#### 2. HTTPS Enforcement
```python
# Force HTTPS redirects
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

#### 3. Cookie Security
```python
# CSRF Cookie Security
CSRF_COOKIE_SECURE = True      # HTTPS only
CSRF_COOKIE_HTTPONLY = True    # No JavaScript access
CSRF_COOKIE_SAMESITE = 'Strict'

# Session Cookie Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600      # 1 hour timeout
```

#### 4. Security Headers
```python
# XSS Protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking Protection
X_FRAME_OPTIONS = 'DENY'

# Referrer Policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```

#### 5. Password Validation
```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.7}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}  # Strong passwords required
    },
    # Additional validators...
]
```

## 👥 User Management

### Creating User Groups

1. **Access Django Admin**
   ```
   http://localhost:8000/admin/
   ```

2. **Create Groups**
   - Navigate to `Groups`
   - Create groups: `Viewers`, `Editors`, `Admins`

3. **Assign Permissions**

   **Viewers Group:**
   - `bookshelf | book | Can view books`

   **Editors Group:**
   - `bookshelf | book | Can view books`
   - `bookshelf | book | Can create books`
   - `bookshelf | book | Can edit books`

   **Admins Group:**
   - All permissions (or make them staff/superuser)

### Adding Users to Groups

1. Go to `Users` in Django admin
2. Select a user
3. In the `Permissions` section:
   - Add user to appropriate groups
   - Set `Staff status` for admin access
   - Set `Superuser status` for full access

## 🔐 Permissions & Groups

### Permission Matrix

| Action | Viewers | Editors | Admins | Staff | Superuser |
|--------|---------|---------|--------|-------|-----------|
| View Books | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create Books | ❌ | ✅ | ✅ | ✅ | ✅ |
| Edit Books | ❌ | ✅ | ✅ | ✅ | ✅ |
| Delete Books | ❌ | ❌ | ✅ | ✅ | ✅ |
| Admin Access | ❌ | ❌ | ❌ | ✅ | ✅ |
| User Management | ❌ | ❌ | ❌ | ❌ | ✅ |

### View Protection Examples

```python
# views.py - Permission decorators
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Only users with 'can_view' permission can access

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # Only users with 'can_edit' permission can access
```

## 🌐 HTTPS & SSL Setup

### Development (Self-Signed Certificate)

```bash
# Generate self-signed certificate (development only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Run with HTTPS
python manage.py runsslserver 0.0.0.0:8443
```

### Production (Nginx + Let's Encrypt)

#### 1. Nginx Configuration

```nginx
# /etc/nginx/sites-available/library-app
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Django App
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static Files
    location /static/ {
        alias /path/to/your/static/files/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files
    location /media/ {
        alias /path/to/your/media/files/;
        expires 7d;
    }
}
```

#### 2. Let's Encrypt SSL

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

#### 3. Production Settings

```python
# settings/production.py
import os

# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database (PostgreSQL recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/library.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🚀 Deployment Guide

### 1. Environment Setup

```bash
# Create environment file
cat > .env << EOF
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=secure_password
DB_HOST=localhost
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EOF
```

### 2. Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `SECRET_KEY` from environment
- [ ] Set up PostgreSQL database
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper static/media file serving
- [ ] Configure email backend
- [ ] Set up monitoring and logging
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Configure error tracking (Sentry)

### 3. Gunicorn Configuration

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn service
sudo nano /etc/systemd/system/library-app.service
```

```ini
[Unit]
Description=Library App Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/library-app.sock LibraryProject.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable library-app
sudo systemctl start library-app
```

## 🧪 Security Testing

### 1. CSRF Testing

```bash
# Test CSRF protection
curl -X POST http://localhost:8000/books/create/ \
  -d "title=Test&author=Author" \
  # Should return 403 Forbidden without CSRF token
```

### 2. Permission Testing

```python
# Test permission decorators
from django.test import TestCase, Client
from django.contrib.auth.models import User

class PermissionTests(TestCase):
    def test_view_without_permission(self):
        user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.client.login(username='testuser', password='password')
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 403)  # Permission denied
```

### 3. Security Headers Testing

```bash
# Test security headers
curl -I https://yourdomain.com/

# Should include:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

### 4. SSL/TLS Testing

```bash
# Test SSL configuration
nmap --script ssl-enum-ciphers -p 443 yourdomain.com

# Use online tools:
# - SSL Labs: https://www.ssllabs.com/ssltest/
# - Security Headers: https://securityheaders.com/
```

## 📝 API Documentation

### Book Search API

```http
GET /api/books/search/?q=search_term
Authorization: Required (Login)
Permission: bookshelf.can_view

Response:
{
  "results": [
    {
      "id": 1,
      "title": "Book Title",
      "author": "Author Name",
      "year": 2023
    }
  ]
}
```

## 🐛 Troubleshooting

### Common Issues

1. **CSRF Token Missing**
   ```
   Error: CSRF verification failed
   Solution: Ensure {% csrf_token %} is in all forms
   ```

2. **Permission Denied**
   ```
   Error: 403 Forbidden
   Solution: Check user permissions and group assignments
   ```

3. **SSL Certificate Issues**
   ```
   Error: SSL certificate verify failed
   Solution: Check certificate installation and renewal
   ```

4. **Static Files Not Loading**
   ```
   Error: 404 on static files
   Solution: Run collectstatic and check STATIC_ROOT
   ```

## 📊 Monitoring & Logging

### Log Files Location
- Application logs: `/var/log/django/library.log`
- Security logs: `/var/log/django/security.log`
- Nginx logs: `/var/log/nginx/`

### Key Metrics to Monitor
- Failed login attempts
- Permission denied errors
- CSRF token failures
- Database query performance
- SSL certificate expiry

## 🔄 Maintenance

### Regular Security Tasks

1. **Weekly:**
   - Review security logs
   - Check for failed login attempts
   - Monitor system updates

2. **Monthly:**
   - Update dependencies
   - Review user permissions
   - Check SSL certificate status

3. **Quarterly:**
   - Security audit
   - Penetration testing
   - Backup testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow security best practices
4. Add tests for new features
5. Update documentation
6. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For security issues, please email: security@yourproject.com
For general support: support@yourproject.com

---

**⚠️ Security Notice:** This application implements security best practices, but security is an ongoing process. Regular updates, monitoring, and security audits are essential for maintaining a secure application.
