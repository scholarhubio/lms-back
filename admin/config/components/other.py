import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECRET_KEY = os.environ.get('SECRET_KEY')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', default="http://127.0.0.1:8000").split(',')

DEBUG = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', default="127.0.0.1,0.0.0.0").split(',')

ROOT_URLCONF = 'config.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

AUTH_USER_MODEL = "users.User"