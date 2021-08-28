"""
Django settings for purbeurre project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import psycopg2.extensions

from pathlib import Path

from dotenv import load_dotenv, find_dotenv  # type: ignore

load_dotenv(find_dotenv())


DB_ORIGIN_BASE_NAME = os.getenv("DB_ORIGIN_BASE_NAME")
DB_ORIGIN_BASE_PASSWD = os.getenv("DB_ORIGIN_BASE_PASSWD")
DB_APP_USER = os.getenv("DB_APP_USER")
HOST = os.getenv("HOST")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4dy(3r1iibs17v1(=+w4ijaob@xgawy4l4c+n$$p034i2k*&-9"

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get("ENV") == "PRODUCTION":
    DEBUG = False
else:
    DEBUG = True

# Dev mode
# ALLOWED_HOSTS = ["127.0.0.1"]

# Prod mode
ALLOWED_HOSTS = ["jlord-purbeurre-p8.herokuapp.com"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "purapps.purbeurre",
    "purapps.purauth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # My Middleware :
    "app.middleware.SearchMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "purapps/purbeurre/templates/pages")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_ORIGIN_BASE_NAME,
        "USER": DB_APP_USER,
        "PASSWORD": DB_ORIGIN_BASE_PASSWD,
        "HOST": HOST,
        "PORT": "5432",
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "TEST": {
            "NAME": "purbeurre_test_database",
        },
        "OPTIONS": {
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "purapps.purauth.authenticate.EmailAuth",
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user
AUTH_USER_MODEL = "purauth.User"

# Redirect to profile URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "registration/profile.html"
