from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# Security settings
# ==============================
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# ==============================
# Installed apps
# ==============================
INSTALLED_APPS = [
    'libraryapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ==============================
# Middleware
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# ==============================
# Templates
# ==============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ==============================
# Database
# ==============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================
# Password validation
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "libraryapp.validators.UppercaseValidator",
    },
    {
        "NAME": "libraryapp.validators.NumberValidator",
    },
]

# ==============================
# Static & Media
# ==============================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ==============================
# Login / Logout redirect
# ==============================
LOGIN_REDIRECT_URL = "libraryapp:book_list"
LOGOUT_REDIRECT_URL = "libraryapp:book_list"

# ==============================
# Email (development mode)
# ==============================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
