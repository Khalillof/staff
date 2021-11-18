
from ..baseSettings import *
import os



DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(" ")

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': os.getenv('POSTGRES_USER', 'user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '')
    }
}

#SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'include_html': True,
    }
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', '')
EMAIL_HOST = os.getenv('EMAIL_HOST','')
EMAIL_PORT = os.getenv('EMAIL_PORT','')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER','')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD','')
SERVER_EMAIL = os.getenv('EMAIL_HOST_USER','')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER','')
DJANGO_SUPERUSER_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DJANGO_SUPERUSER_EMAIL = os.getenv('EMAIL_HOST_USER', '')