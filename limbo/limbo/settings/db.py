import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", None),
        "USER": os.getenv("POSTGRES_USER", None),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", None),
        "HOST": os.getenv("POSTGRES_HOST", None),
        "PORT": "5432",
    }
}
