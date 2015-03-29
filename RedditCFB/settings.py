"""
Django settings for RedditCFB project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '00=508^phx1^_@!+baf+k73spdi&8jgd-(4a!!z5t#(=ee_i&3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'south',
    'commentfilter',



)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'RedditCFB.urls'

WSGI_APPLICATION = 'RedditCFB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#Offline Database
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#      }
#  }

#Database for PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gardnmi$redditflair',
        'USER': 'gardnmi',
        'PASSWORD': '9643602Mjg',
        'HOST': 'mysql.server',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

############################Non-Standard Settings############################
# Template Location
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,"static", "templates"),
    #Goes one level up src and adds folder location static/templates/
)

# When Live use if not DEBUG
#if not DEBUG:
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR,"static", "static-only")
MEDIA_ROOT = os.path.join(BASE_DIR,"static", "media")
STATICFILES_DIRS = (
        os.path.join(BASE_DIR,"static", "static"),
    )

#for endless pagination
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

#Need for Heroku uncomment DATABASE below when live and comment the local DATABASE above
#import dj_database_url
#DATABASES = {}
#DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')




