"""
Django settings for Railway deployment.
"""
from .base import *
import dj_database_url

# SECURITY
DEBUG = False
ALLOWED_HOSTS = ['*']  # Railway will handle this

# Database
# Railway provides DATABASE_URL automatically
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Security settings for production
SECURE_SSL_REDIRECT = False  # Railway handles SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
