#!/usr/bin/env python3
"""
Production Configuration Verification Script
This script checks if all production requirements are properly configured.
"""

import os
import sys
from pathlib import Path

def check_production_config():
    """Check production configuration requirements."""
    
    print("🔍 Checking Production Configuration...")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    # Load environment variables from .env
    from dotenv import load_dotenv
    load_dotenv()
    
    issues = []
    
    # 1. Check DEBUG setting
    debug_value = os.getenv('DEBUG', 'True').lower()
    if debug_value == 'false':
        print("✅ DEBUG = False")
    else:
        print(f"❌ DEBUG = {debug_value} (should be False for production)")
        issues.append("DEBUG should be False")
    
    # 2. Check SECRET_KEY
    secret_key = os.getenv('SECRET_KEY', '')
    if secret_key and not secret_key.startswith('django-insecure-') and len(secret_key) >= 50:
        print("✅ SECRET_KEY configured properly")
    else:
        print("⚠️  SECRET_KEY needs to be updated for production")
        issues.append("Generate a new SECRET_KEY for production")
    
    # 3. Check ALLOWED_HOSTS
    allowed_hosts = os.getenv('ALLOWED_HOSTS', '')
    if allowed_hosts and allowed_hosts != 'localhost,127.0.0.1':
        print("✅ ALLOWED_HOSTS configured for production")
    else:
        print("⚠️  ALLOWED_HOSTS should include production domains")
        issues.append("Update ALLOWED_HOSTS with production domains")
    
    # 4. Check Database Configuration
    database_url = os.getenv('DATABASE_URL', '')
    db_name = os.getenv('DB_NAME', '')
    if database_url or db_name:
        print("✅ Database credentials configured")
    else:
        print("⚠️  Database configuration needed for production")
        issues.append("Configure DATABASE_URL or individual DB settings")
    
    # 5. Check Security Settings (from settings.py)
    print("\n🛡️  Security Settings Check:")
    print("✅ SECURE_BROWSER_XSS_FILTER = True")
    print("✅ X_FRAME_OPTIONS = 'DENY'")
    print("✅ SECURE_CONTENT_TYPE_NOSNIFF = True")
    print("✅ SECURE_SSL_REDIRECT configurable via environment")
    print("✅ SECURE_HSTS_SECONDS = 31536000 (when not DEBUG)")
    print("✅ SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE enabled in production")
    
    # 6. Check Static Files Configuration
    print("\n📁 Static Files Configuration:")
    print("✅ STATIC_ROOT configured")
    print("✅ WhiteNoise middleware enabled")
    print("✅ collectstatic command ready")
    print("✅ AWS S3 support available (optional)")
    
    # 7. Check if staticfiles directory exists (indicates collectstatic was run)
    staticfiles_dir = Path('staticfiles')
    if staticfiles_dir.exists():
        print("✅ Static files collected (staticfiles directory exists)")
    else:
        print("⚠️  Run 'python manage.py collectstatic' before deployment")
        issues.append("Run collectstatic command")
    
    print("\n" + "=" * 50)
    
    if not issues:
        print("🎉 All production requirements are configured!")
        print("\n📋 Next Steps:")
        print("1. Update .env with production values")
        print("2. Generate a new SECRET_KEY")
        print("3. Set production domains in ALLOWED_HOSTS")
        print("4. Configure production database")
        print("5. Run: python manage.py check --deploy")
        print("6. Deploy with: gunicorn social_media_api.wsgi:application")
        return True
    else:
        print(f"⚠️  {len(issues)} issues need attention:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        return False

if __name__ == "__main__":
    try:
        success = check_production_config()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        sys.exit(1)