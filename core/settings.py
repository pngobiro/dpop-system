import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_hardcoded_secret_key_here' # IMPORTANT: Replace with a strong, unique key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = 'authentication:login'  # Correct
# or
LOGIN_URL = '/accounts/login/' # Correct - explicitly specifies

# allow all hosts in development
ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost','www.dspop.info']


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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dspop',
        'USER': 'dspop_user',
        'PASSWORD': 'dspop_password_2025',
        'HOST': '172.27.0.2',
        'PORT': '5432',
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Point to the correct volume mount
MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

ASSETS_ROOT = '/static/assets'


# FILE_UPLOAD_MAX_MEMORY_SIZE 8GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 8589934592



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

OPENAI_API_KEY = 'your_openai_api_key_here'


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
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Google Drive settings
GOOGLE_DRIVE_CREDENTIALS_FILE = os.path.join(BASE_DIR, os.environ.get('GOOGLE_DRIVE_CREDENTIALS_FILE', 'client_secrets.json'))
GOOGLE_DRIVE_DOCUMENT_ROOT = os.environ.get('GOOGLE_DRIVE_DOCUMENT_ROOT', '')  # Root folder ID for documents

# Google Drive API scopes
GOOGLE_DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly'
]

# Check if credentials file exists
if not os.path.exists(GOOGLE_DRIVE_CREDENTIALS_FILE):
    print(f"Warning: Google Drive credentials file not found at {GOOGLE_DRIVE_CREDENTIALS_FILE}")



# Add Webpack loader settings
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'js/dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pngobiro@gmail.com'
EMAIL_HOST_PASSWORD = 'woww sfla ibib gsjh'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'DSPOP System <pngobiro@gmail.com>'

