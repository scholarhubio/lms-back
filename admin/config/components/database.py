import os

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': os.environ.get('CONTENT_POSTGRES_DB_NAME'),
        'USER': os.environ.get('CONTENT_POSTGRES_USER'),
        'PASSWORD': os.environ.get('CONTENT_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('CONTENT_POSTGRES_HOST'),
        'PORT': os.environ.get('CONTENT_POSTGRES_PORT'),
        'OPTIONS': {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            'options': '-c search_path=public'
        }
    }
}
