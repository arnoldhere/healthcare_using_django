"""
Django settings for healthcareproject project.

Generated by 'django-admin startproject' using Django 4.1.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import pymongo

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6iv17%asiv(a2e1$-(6oq%a!k(3p_r@s%$+m)pwzf%xseek3+z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'healthcareapp',
    'customAdmin',
    'staffApp',
    'toastmessage',
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

ROOT_URLCONF = 'healthcareproject.urls'

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
# CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'

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

WSGI_APPLICATION = 'healthcareproject.wsgi.application'

AUTH_USER_MODEL = 'healthcareapp.UserModel'
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'healthcareApp',
        # 'USER': 'root',
        # 'password': '',
        'HOST': 'localhost',
        'PORT': '27017'
        # 'ENFORCE_SCHEMA': False,
        # 'CLIENT': {
        #     'host': "mongodb://localhost:27017/",
        #     'port': 27017,
        #     'authSource': 'healthcare_app_django'
        # },
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'LoginPage'  # Replace 'login' with your login URL name

# APPEND_SLASH = False



# EMAIL CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # use the SMTP for current email configs
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server for Gmail
EMAIL_PORT = 587  # Port for TLS (587 for TLS, 465 for SSL)
EMAIL_USE_TLS = True  # Use TLS for secure connection

#EMAIL CREDENTIALS
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = "" # APP PASSWORD
# DEFAULT_FROM_EMAIL = "official.arnold.mac.2004@gmail.com"
