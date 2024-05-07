from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db_adopta",
        "USER": "root",
        "PASSWORD": "Appdopta*1",
        "HOST": "appdopta-aws.cdw28ekqc8xz.us-east-2.rds.amazonaws.com",
        "PORT": "3306",
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
