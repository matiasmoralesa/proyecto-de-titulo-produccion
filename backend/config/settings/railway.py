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
    'proyecto-de-titulo-produccion.vercel.app',
    '*.vercel.app',
    'localhost',
    '127.0.0.1'
]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://proyecto-de-titulo-produccion-production.up.railway.app',
    'https://*.railway.app',
    'https://proyecto-de-titulo-produccion.vercel.app',
    'https://*.vercel.app',
]

# CORS Settings - TEMPORARY: Allow all origins for debugging
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

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

# Logging configuration for Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.omnichannel_bot': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Nivel DEBUG para ver todos los logs del bot
            'propagate': False,
        },
    },
}
