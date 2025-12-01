"""
Django settings for Railway deployment.
"""
from .base import *
import dj_database_url
import os

# SECURITY
DEBUG = False
ALLOWED_HOSTS = [
    'proyecto-de-titulo-produccion-production.up.railway.app',
    '*.railway.app',
    'proyecto-de-titulo-produccion-btez6tjht.vercel.app',
    '*.vercel.app',
    'localhost',
    '127.0.0.1'
]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://proyecto-de-titulo-produccion-production.up.railway.app',
    'https://*.railway.app',
    'https://proyecto-de-titulo-produccion-btez6tjht.vercel.app',
    'https://*.vercel.app',
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://proyecto-de-titulo-produccion-btez6tjht.vercel.app',
    'https://proyecto-de-titulo-produccion-production.up.railway.app',
]
CORS_ALLOW_CREDENTIALS = True

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
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
