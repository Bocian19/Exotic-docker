import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = ['51.83.129.163', '0.0.0.0']
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(','))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'carparts',
    'captcha',
    'imagekit',
    'robots',

]

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

DATABASES = {
    'default': {
        'HOST': os.getenv('POSTGRES_HOST', default=""),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME', default=""),
        'USER': os.getenv('POSTGRES_USER', default=""),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default=""),
        'PORT': 5432,
    }
}

ROOT_URLCONF = 'Exotic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Exotic.wsgi.application'

SITE_ID = 1


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = '/static/media/'
STATIC_URL = '/static/static/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'


INTERNAL_IPS = [
    # ...
    # '127.0.0.1',
    # ...
]


SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')

RECAPTCHA_PUBLIC_KEY='6LeYu-EZAAAAAAZP3Ggbe1Q6uk7eHob2xaO9Rgi7'


try:
    from .email_credentials import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_TLS,\
         DEFAULT_FROM_EMAIL, EMAIL_USE_SSL, EMAIL_BACKEND, RECAPTCHA_PRIVATE_KEY
except ModuleNotFoundError:
    print("Brak podanych informacji w pliku email_credentials.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)