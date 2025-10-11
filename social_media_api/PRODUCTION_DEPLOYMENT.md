# Production Deployment Guide

## Production Configuration Checklist

### ✅ Security Settings
- [x] DEBUG = False
- [x] SECURE_BROWSER_XSS_FILTER = True
- [x] X_FRAME_OPTIONS = 'DENY'
- [x] SECURE_CONTENT_TYPE_NOSNIFF = True
- [x] SECURE_SSL_REDIRECT configured via environment
- [x] SECURE_HSTS_SECONDS = 31536000
- [x] SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE enabled in production

### ✅ Database Configuration
- [x] PostgreSQL support via DATABASE_URL
- [x] Individual database credential support
- [x] Fallback to SQLite for development

### ✅ Static and Media Files
- [x] WhiteNoise configured for static files
- [x] AWS S3 support for static and media files (optional)
- [x] Proper STATIC_ROOT and MEDIA_ROOT configuration
- [x] collectstatic command ready

### ✅ Additional Production Features
- [x] Logging configuration with file output
- [x] Email backend configuration
- [x] CORS configuration for production origins
- [x] Environment-based configuration

## Deployment Steps

### 1. Environment Setup
```bash
# Copy and configure production environment
cp .env.production .env
# Edit .env with your production values
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 5. Security Checklist
```bash
# Run Django's security check
python manage.py check --deploy
```

### 6. Start Production Server
```bash
# Using Gunicorn (recommended)
gunicorn social_media_api.wsgi:application --bind 0.0.0.0:8000

# Or for development testing
python manage.py runserver 0.0.0.0:8000
```

## Environment Variables Reference

### Required for Production
- `SECRET_KEY`: Django secret key (generate a new one!)
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: PostgreSQL connection string

### Optional
- `SECURE_SSL_REDIRECT`: Enable HTTPS redirect (`True`/`False`)
- `USE_S3`: Enable AWS S3 storage (`True`/`False`)
- `AWS_*`: AWS S3 configuration variables
- `EMAIL_*`: Email configuration variables
- `CORS_ALLOWED_ORIGINS`: Frontend domains

## AWS S3 Setup (Optional)

1. Create S3 bucket
2. Configure bucket policy for public read access to static files
3. Set environment variables:
   - `USE_S3=True`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_STORAGE_BUCKET_NAME`
   - `AWS_S3_REGION_NAME`

## SSL/HTTPS Configuration

For production with HTTPS:
```env
SECURE_SSL_REDIRECT=True
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Monitoring and Logs

- Logs are written to `logs/django.log` in production
- Monitor the application using the configured logging
- Check Django admin at `/admin/` for application monitoring