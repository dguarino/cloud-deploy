"""
Django settings for resource_manager project.

"""

import os
import sys
import hbp_app_python_auth.settings as auth_settings

ENV = os.environ.get('NMPI_ENV', 'production')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'none')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') in ['True', '1']
LOCAL_DB = True  # only applies when ENV='dev'

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quotas',
    'social.apps.django_app.default',
]
if ENV == "dev":
    INSTALLED_APPS.append('sslserver')
    sys.path.append("..")

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'hbp_app_python_auth.auth.HbpAuth',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'resource_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['app/templates', 'coordinator_app/templates'],
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

WSGI_APPLICATION = 'resource_manager.wsgi.application'

APPEND_SLASH = False

# Database

if ENV == "dev" and LOCAL_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'nmpi',
            'USER': 'nmpi_dbadmin',
            'PASSWORD': os.environ.get("NMPI_DATABASE_PASSWORD"),
            'HOST': os.environ.get("NMPI_DATABASE_HOST"),
            'PORT': os.environ.get("NMPI_DATABASE_PORT", "5432"),
        },
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = "%s/static/" % BASE_DIR
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "lib"),
    os.path.join(BASE_DIR, "app"),
    os.path.join(BASE_DIR, "coordinator_app"),
]


HBP_COLLAB_SERVICE_URL = 'https://services.humanbrainproject.eu/collab/v0/'
HBP_ENV_URL = 'https://collab.humanbrainproject.eu/config.json'
HBP_IDENTITY_SERVICE_URL = 'https://services.humanbrainproject.eu/idm/v1/api'


SOCIAL_AUTH_HBP_KEY = auth_settings.SOCIAL_AUTH_HBP_KEY = os.environ.get('HBP_OIDC_CLIENT_ID')
SOCIAL_AUTH_HBP_SECRET = auth_settings.SOCIAL_AUTH_HBP_SECRET = os.environ.get('HBP_OIDC_CLIENT_SECRET')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'quotas': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        },
    },
}
if ENV == "dev":
    LOGGING['handlers']['file']['filename'] = 'django.log'