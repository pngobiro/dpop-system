import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x-7z@n$vgndj+lp*g98&*!#z2shsgah6jgt(%%k1f_%q4@nm9r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = 'authentication:login'  # Correct
# or
LOGIN_URL = '/accounts/login/' # Correct - explicitly specifies

# allow all hosts in development
ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost','69f8-196-202-207-77.ngrok-free.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # Added for template filters like intcomma
    'authentication', # added the authentication apps
    'apps.permissions',
    'apps.home',
    # 'django_unicorn', # Removed as Unicorn is no longer used
    'apps.statistics',
    'apps.document_management',
    'apps.organization',
    'apps.budget',
    'apps.meetings',
    'apps.innovations',
    'apps.memos',
    'apps.mail',
    'apps.pmmu',
    'apps.tasks', # Added the tasks app

    # Third-party apps
    'debug_toolbar',
    'crispy_forms',
    'crispy_bootstrap5',

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


AUTH_USER_MODEL = 'authentication.CustomUser'




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "statistics:home"  # Route defined in statistics/urls.py
LOGOUT_REDIRECT_URL = "statistics:home"  # Route defined in statistics/urls.py
TEMPLATE_DIR = os.path.join(BASE_DIR, "apps/templates")  # ROOT dir for templates

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # templates dir then apps
            TEMPLATE_DIR,
            os.path.join(TEMPLATE_DIR, "apps"),
        ],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Point to the correct volume mount
MEDIA_URL = '/media/'


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

ASSETS_ROOT = '/static/assets'


# FILE_UPLOAD_MAX_MEMORY_SIZE 8GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 8589934592



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# coomand tto create new migrations using docker-compose
# docker-compose run web python manage.py makemigrations



# Enable logging in all environments
# https://docs.djangoproject.com/en/3.2/topics/logging/#configuring-logging

import os

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


# Google Drive settings
GOOGLE_OAUTH_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')
GOOGLE_OAUTH_REDIRECT_URI = 'http://your-domain/documents/google-auth-callback/'


# Add Webpack loader settings
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'js/dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


# Update STATICFILES_DIRS
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]