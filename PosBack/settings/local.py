from .base import *

DEBUG = True

INSTALLED_APPS += [
    # Third-party apps
    'django_extensions',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default Port
    "http://localhost:8000",  # Django default Port
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",  # React default Port
]
