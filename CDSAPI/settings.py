"""
Django settings for CDSAPI project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
#-------------------------------------------------------------->
# SETTING UTILITIES
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


#-------------------------------------------------------------->
# GENERAL DJANGO SETTINGS - (WSGI, URLS, MIDDLEWARE, APPS, ETC)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

from django.utils import crypto
SECRET_KEY = os.environ.get("SECRET_KEY", crypto.get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'kitbuilder',
    'kitbuilder.kitbuilder_beta',
    'kitbuilder.kitbuilder_v1',
    'useraccount',
    'userprofile',
    'api',
    'provider',
    'provider.oauth2',
    'corsheaders',
    'tinymce',
    'herokuapp',
    'import_export',
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CDSAPI.urls'

WSGI_APPLICATION = 'CDSAPI.wsgi.application'


#-------------------------------------------------------------->
# DATABASE SETTINGS

#Below is HEROKU setup for database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd7pajl538fmet1',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'lhozmsincrgdwf',
        'PASSWORD': '60-_sD2L9K3TjJLIrLocDBx7J8',
        'HOST': 'ec2-174-129-197-200.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}
# import dj_database_url
# DATABASES = {'default': dj_database_url.config(default='postgres://lhozmsincrgdwf:60-_sD2L9K3TjJLIrLocDBx7J8@ec2-174-129-197-200.compute-1.amazonaws.com:5432/d7pajl538fmet1')}


#-------------------------------------------------------------->
# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEBUG = True

TEMPLATE_DEBUG = DEBUG

#-------------------------------------------------------------->
# TEMPLATE/STATIC FILE FINDERS AND DIRECTORIES
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, 'CustomDrumSamples/static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    os.path.join(BASE_DIR, "provider/templates"),
#    os.path.join(BASE_DIR, "templates/registration"),
#    os.path.join(BASE_DIR, "templates/courses"),
#    os.path.join(BASE_DIR, "templates/userlogin"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#-------------------------------------------------------------->
# DJANGO REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_oauth.authentication.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '10000/day',
    },
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

#-------------------------------------------------------------->
# DJANGO CORS SETTINGS

# NOTE: HAVE TO CHANGE line 491 of provider/views.py in site-packages to use content_type instead of mime_type for this
# to work in Django 1.7 and later.
# curl -X POST -d 'client_id=0f4d3a53f1db12be80cd&client_secret=d5fdf1e1a0fdc057844dfebe5f795cfe7d2d187e&grant_type=password&username=maddenmoment@gmail.com&password=123456' 'http://127.0.0.1:8000/oauth2/access_token'
CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:4200',
    'fierce-depths-3755.herokuapp.com',
    #'hostname.example.com'
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

#-------------------------------------------------------------->
# DJOSER/AUTHENTICATION SETTINGS
AUTH_USER_MODEL = 'useraccount.User'

DJOSER = {
    'DOMAIN': 'fierce-depths-3755.herokuapp.com',
    'SITE_NAME': 'Beat Paradigm',
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'ACTIVATION_URL': 'registration/activate/{uid}/{token}',
    'ACCOUNT_UPDATE_CONFIRM_URL': 'account-settings/update-info/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

#-------------------------------------------------------------->
# EMAIL SETTINGS
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME", "")
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD", "")
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "info@beatparadigm.com"
USE_SENDGRID = True

#-------------------------------------------------------------->
# STRIPE SETTINGS
STRIPE_PUBLISHABLE = 'pk_test_hyDepohZLg2M8UX2pYG6nhRI'
STRIPE_SECRET = 'sk_test_ONEo51glZMcLXv66UzPDWSru'

# Allow all host headers
ALLOWED_HOSTS = ['*']

#-------------------------------------------------------------->
# AMAZON S3 SETTINGS
USE_AMAZON_S3 = True
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_AUTO_CREATE_BUCKET = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}
AWS_S3_FILE_OVERWRITE = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False

#-------------------------------------------------------------->
# CACHE SETTINGS
# CACHES = {
#     # Long cache timeout for staticfiles, since this is used heavily by the optimizing storage.
#     "staticfiles": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "TIMEOUT": 60 * 60 * 24 * 365,
#         "LOCATION": "staticfiles",
#     },
# }

#-------------------------------------------------------------->
# MEDIA FILE STORAGE SETTINGS
# Use Amazon S3 for storage for uploaded media files.
import custom_storages
# DEFAULT_FILE_STORAGE = "custom_storages.MediaStorage" --> Using the storage in amazon_file_field module
# MEDIA_ROOT = 'media'
MEDIA_URL = 'https://%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME, custom_storages.MEDIAFILES_LOCATION)


#-------------------------------------------------------------->
# STATIC FILE STORAGE SETTINGS
# Use Amazon S3 for static files storage.
STATIC_ROOT = ""
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = 'https://%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME, custom_storages.STATICFILES_LOCATION)


#-------------------------------------------------------------->
# DJANGO TINY MCE SETTINGS
TINYMCE_JS_URL = MEDIA_URL + "tinymce/tinymce.min.js"
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "advlist autolink lists link image charmap print preview hr anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table contextmenu directionality emoticons template paste textcolor colorpicker textpattern",
    'theme': "modern",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False


#-------------------------------------------------------------->
# LOGGING SETTINGS
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

#-------------------------------------------------------------->
# SSL/SSLIFY SETTINGS
SSLIFY_DISABLE = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#-------------------------------------------------------------->
# LOCAL SETTINGS IMPORT
try:
    from local_settings import *
except ImportError as e:
    pass