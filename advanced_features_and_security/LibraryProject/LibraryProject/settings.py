"""
Django settings for LibraryProject with enhanced security configurations.

This settings file implements comprehensive security measures including:
- Custom User Model
- HTTPS enforcement
- Security headers
- Content Security Policy (CSP)
- CSRF protection
- Session security
- Database security
- File upload security

For production deployment, ensure all security settings are properly configured
and regularly review security best practices.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# In production, this should be loaded from environment variables
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Set to False for security in production
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Allowed hosts for security - restrict to your domain in production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================

# Use our custom user model instead of Django's default
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps for security
    'csp',  # Content Security Policy
    # Local apps
    'bookshelf',
]

MIDDLEWARE = [
    # Security middleware should be at the top
    'django.middleware.security.SecurityMiddleware',
    # Session middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS and common middleware
    'django.middleware.common.CommonMiddleware',
    # CSRF protection middleware - CRITICAL for security
    'django.middleware.csrf.CsrfViewMiddleware',
    # Authentication middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Messages middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    # Clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Content Security Policy middleware
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # SQLite-specific options
        'OPTIONS': {
            'timeout': 20,
        },
    }
}

# =============================================================================
# PASSWORD VALIDATION - Enhanced Security
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'email', 'first_name', 'last_name'),
            'max_similarity': 0.7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Require strong passwords
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES AND MEDIA
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (user uploads) - secure configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# =============================================================================
# HTTPS AND SSL SECURITY SETTINGS
# =============================================================================

# Force HTTPS in production
SECURE_SSL_REDIRECT = not DEBUG  # Only redirect to HTTPS in production

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure proxy settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =============================================================================
# COOKIE SECURITY
# =============================================================================

# CSRF Cookie Security
CSRF_COOKIE_SECURE = not DEBUG  # Only send over HTTPS in production
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access
CSRF_COOKIE_SAMESITE = 'Strict'  # Prevent CSRF attacks
CSRF_COOKIE_AGE = 3600  # 1 hour

# Session Cookie Security
SESSION_COOKIE_SECURE = not DEBUG  # Only send over HTTPS in production
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevent session hijacking
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # End session when browser closes

# =============================================================================
# SECURITY HEADERS
# =============================================================================

# XSS Protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking Protection
X_FRAME_OPTIONS = 'DENY'  # Prevent framing entirely

# Referrer Policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# =============================================================================
# CONTENT SECURITY POLICY (CSP)
# =============================================================================

# Updated CSP configuration for django-csp 4.0+
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'"),  # Allow inline scripts for forms
        'style-src': ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com"),
        'font-src': ("'self'", "https://fonts.gstatic.com"),
        'img-src': ("'self'", "data:", "https:"),
        'connect-src': ("'self'",),
        'frame-src': ("'none'",),
        'object-src': ("'none'",),
        'base-uri': ("'self'",),
        'form-action': ("'self'",),
    }
}

# Report CSP violations (in production, set up a reporting endpoint)
# CSP_REPORT_URI = '/csp-report/'

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'bookshelf': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# =============================================================================
# AUTHENTICATION SETTINGS
# =============================================================================

# Login URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Password reset settings (for production, configure email backend)
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour

# =============================================================================
# EMAIL CONFIGURATION (for production)
# =============================================================================

# In production, configure proper email backend for password resets
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Configure for production email service
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# =============================================================================
# CACHE CONFIGURATION
# =============================================================================

# Use Redis in production for better security and performance
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CUSTOM SECURITY SETTINGS
# =============================================================================

# Rate limiting (implement with django-ratelimit in production)
# RATELIMIT_ENABLE = True

# Additional security headers
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# =============================================================================
# PRODUCTION SECURITY CHECKLIST
# =============================================================================

"""
PRODUCTION DEPLOYMENT SECURITY CHECKLIST:

1. Environment Variables:
   - Set SECRET_KEY from environment
   - Set DEBUG=False
   - Configure ALLOWED_HOSTS properly
   - Set database credentials securely

2. HTTPS Configuration:
   - Install SSL certificate
   - Configure web server (Nginx/Apache) for HTTPS
   - Test SSL configuration

3. Database Security:
   - Use PostgreSQL in production
   - Configure database user permissions
   - Enable database logging
   - Regular backups with encryption

4. Server Security:
   - Regular security updates
   - Configure firewall
   - Disable unnecessary services
   - Monitor system logs

5. Application Security:
   - Regular dependency updates
   - Security testing
   - Code reviews
   - Penetration testing

6. Monitoring:
   - Set up error tracking (Sentry)
   - Configure log monitoring
   - Set up alerts for security events
   - Regular security audits

7. Backup and Recovery:
   - Automated encrypted backups
   - Test recovery procedures
   - Document incident response plan
"""
