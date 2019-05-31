import secrets
from dotenv import load_dotenv
from pathlib import Path
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

# Reading configuration from environment file
env_path = Path("{0}/../".format(BASE_DIR)) / '.env'
load_dotenv(dotenv_path=env_path)

db_type = os.getenv("DB_TYPE")
if db_type == 'sqlite':
    db_name = os.getenv("DB_FILE_NAME")
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, db_name),
        }
    }
elif db_type == 'mysql':
    # Database
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_USER_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        }
    }
else:
    print("- Error: DB Type not specified. Please edit your .env file and specify proper DB Type ( sqlite, mysql, postgres)")
    exit(1)

# Emails

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

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
            'level': 'DEBUG',
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
