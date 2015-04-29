"""
Django settings for CDSAPI project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5%d2#7=3jq1ad$+!u7j2_e206gjmc84yf)^ch&#6$4(4k&u864'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
)

MIDDLEWARE_CLASSES = (
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


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#Below is Development setup for database
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'cdstestdb',                      # Or path to database file if using sqlite3.
#         # The following settings are not used with sqlite3:
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',                      # Set to empty string for default.
#     }
# }

#Below is HEROKU setup for database
#
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

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Static Root is where the production server finds the static files
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "assets")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, 'CustomDrumSamples/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'


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
        'user': '1000/day',
    },
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

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

AUTH_USER_MODEL = 'useraccount.User'

DJOSER = {
    'DOMAIN': 'https://fierce-depths-3755.herokuapp.com',
    'SITE_NAME': 'Custom Drum Samples',
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'ACTIVATION_URL': 'registration/activate/{uid}/{token}',
    'ACCOUNT_UPDATE_CONFIRM_URL': 'account-settings/update-info/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

# Had to change this email account's security settings for testing purposes
# go to https://www.google.com/settings/security/lesssecureapps to change back.
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bant7205@gmail.com'
EMAIL_HOST_PASSWORD = 'UBM071105'
EMAIL_PORT = 587

# Example Registration
# curl -X POST http://127.0.0.1:8000/api/accounts/register --data 'username=bant7205&email=bant7205@gmail.com&password=654321'

# Stripe Settings for Pro Essentials --> Change when ready.
STRIPE_PUBLISHABLE = 'pk_test_hyDepohZLg2M8UX2pYG6nhRI'
STRIPE_SECRET = 'sk_test_ONEo51glZMcLXv66UzPDWSru'

#CSRF_COOKIE_NAME = 'mycsrftoken'
# curl -X POST http://127.0.0.1:8000/api/custom-kits/purchase/ --data 'userID=1&kitName=NewCustomKit&samples=[1]'

# *********** HEROKU SETTINGS *************
# Parse database configuration from $DATABASE_URL
# import dj_database_url
# DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# hosted at https://cryptic-harbor-4037.herokuapp.com/
# Heroku remote at https://git.heroku.com/cryptic-harbor-4037.git

TINYMCE_JS_URL = MEDIA_URL + "tinymce/tinymce.min.js"
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "advlist autolink lists link image charmap print preview hr anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table contextmenu directionality emoticons template paste textcolor colorpicker textpattern",
    'theme': "modern",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False
