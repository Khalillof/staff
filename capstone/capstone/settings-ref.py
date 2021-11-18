import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

INSTALLED_APPS = [
    'news',
    'agency',
    'accounts',
    'mail',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'capstone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'capstone.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('POSTGRES_DB', os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': os.environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = os.environ['SERVER_EMAIL']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

LOGIN_REDIRECT_URL = '/'
#LOGOUT_REDIRECT_URL = '/'
PASSWORD_RESET_TIMEOUT = 86400 # one day

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "agency/static/upload/")


FIXTURE_DIRS =['capstone'] # python manage.py loaddata seed_db.json

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")

DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SU_NAME')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SU_EMAIL')

CACHE_MIDDLEWARE_SECONDS=600

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_AGE	= 31449600
CSRF_COOKIE_DOMAIN	= None
CSRF_COOKIE_HTTPONLY=False
CSRF_COOKIE_NAME='csrftoken'
CSRF_COOKIE_PATH='/'
CSRF_COOKIE_SAMESITE='Lax'
CSRF_COOKIE_SECURE	= True
CSRF_HEADER_NAME='HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS=[]
CSRF_USE_SESSIONS=False

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