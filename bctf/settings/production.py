import secrets
from .base import *
from .email import *
from .uptime import *

# SECURITY WARNING: keep the secret key used in production secret! This will try to get secret key from environment varaible.
# If that fails it will create .secret_key file for you, and populate it with random secured SECRET_KEY token.
if not os.environ.get('SECRET_KEY'):
    try:
        with open('.secret_key', 'rb') as secret_key:
            SECRET_KEY = secret_key.read()
    except (OSError, IOError):
        SECRET_KEY = None

    if not SECRET_KEY:
        SECRET_KEY = secrets.token_urlsafe(50)
        try:
            with open('.secret_key', 'w') as secret_key:
                secret_key.write(SECRET_KEY)
                secret_key.flush()
        except (OSError, IOError):
            pass
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*', ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/bctf_cache',
    }
}

# Security

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/tmp/bctf-prod.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
