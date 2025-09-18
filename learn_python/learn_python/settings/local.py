from .base import *
from ..env import BASE_DIR

from decouple import config
import cloudinary
import cloudinary.uploader
import cloudinary.api

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t61lw+rqf$&a2qr&m2hnn66!bz*0s)w09@0r3=lebrkm$2l+g5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"



# Cloudinary config (use your own credentials)
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
    "CLOUDINARY_URL": config("CLOUDINARY_URL"),
    "DEFAULT_FOLDER": "audio",
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]