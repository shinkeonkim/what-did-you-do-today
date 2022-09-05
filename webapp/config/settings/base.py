"""
Django settings for what_did_you_do_today project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

import environ
from config.utils import create_directory_if_not_exists, create_file_if_not_exists

PROJECT_DIR = environ.Path(__file__) - 3

env = environ.Env(DEBUG=(bool, False))

env.read_env(f'{PROJECT_DIR}/.env')

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PACKAGE_APPS = []

PROJECT_APPS = [
    'user',
]

INSTALLED_APPS = DJANGO_APPS + PACKAGE_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = f'{PROJECT_DIR}/static/'

STATICFILES_DIRS = [f'{PROJECT_DIR}/user/staticfiles/']

MEDIA_URL = '/media/'
MEDIA_ROOT = f'{PROJECT_DIR}/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

LOG_DIR_PATH = os.path.join(PROJECT_DIR, 'logs/')
SQL_LOG_FILE_PATH = os.path.join(PROJECT_DIR, 'logs/sql_logfile.log')
WEB_LOG_FILE_PATH = os.path.join(PROJECT_DIR, 'logs/logfile.log')

create_directory_if_not_exists(str(LOG_DIR_PATH))
create_file_if_not_exists(str(SQL_LOG_FILE_PATH))
create_file_if_not_exists(str(WEB_LOG_FILE_PATH))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logFormat': {
            'format': '{levelname} ... [{name}:{lineno}] {asctime} {message}',
            'datefmt': '%d/%b/%Y %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'sql_logger': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'logFormat',
        },
        'web_logger': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'logFormat',
        },
        'sql_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': SQL_LOG_FILE_PATH,
            'formatter': 'logFormat',
        },
        'web_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': WEB_LOG_FILE_PATH,
            'formatter': 'logFormat',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': [
                'sql_logger',
                'web_logger',
                'sql_log_file',
                'web_log_file',
            ],
            'level': 'DEBUG',
            'formatter': 'logFormat',
        },
    },
}
