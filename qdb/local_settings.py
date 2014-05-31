from settings import *

SECRET_KEY = 'this is not the real key'

DEBUG = True

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'qdb',
        'USER': 'tristan',
        'PASSWORD': 'postgresql',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

PASSWORD_REQUIRED_PASSWORD = 'password'
