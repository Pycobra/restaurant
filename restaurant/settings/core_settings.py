from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-5!q(lb_zwd-k55ua7##t2!tr(%c@@^!gu44lsf2aw_0(1s^o(b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


AUTH_USER_MODEL='account.UserBase'
LOGIN_URL='account_:login'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL='account_:login'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'chats'

SUBCRIPTION_TIMEOUT = 3


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
    'apps.account',
    'apps.product',
    'apps.order',
    'apps.cart',
    'apps.checkout',
    'mptt',
]

PAYSTACK_PUBLIC_KEY = 'pk_test_1bd3d130cbb6f84a90e8cdb0e13a82a659ebbedc'
PAYSTACK_SECRET_KEY = 'sk_test_8c231ece81620c5dfe92377a418f6165acec884d'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant.urls'

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
                'apps.cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurant.wsgi.application'


"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'restaurantDB',
        'USER': 'postgres',
        "PASSWORD": 'guht9876',
        "HOST": 'localhost',
        "PORT": '5432',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS=[
    BASE_DIR / 'static'
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MPTT_ADMIN_LEVEL_INDENT = 20

