from .base import *
from .email import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z6u+3oksy50%8xepzcrgc&1t3mgjd6)oy=qyqm-hb5-j*3a=q@'

DEBUG = False

ALLOWED_HOSTS = ['*', ]

STATIC_ROOT = "/var/tmp/static"
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media/')

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
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
