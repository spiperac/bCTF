from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z6u+3oksy50%8xepzcrgc&1t3mgjd6)oy=qyqm-hb5-j*3a=q@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]

if DEBUG == True:
    INSTALLED_APPS += [
        'django.contrib.admin', 
        'debug_toolbar',                
    ]

    MIDDLEWARE += [
        # ...
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        # ...
    ]

    INTERNAL_IPS = ('127.0.0.1', )

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
            'filename': '/tmp/bctf-dev.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Development settings
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")