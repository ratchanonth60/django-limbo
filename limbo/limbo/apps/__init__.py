BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MY_APPS = [
    "limbo.apps.users",
    "limbo.apps.address",
]

INSTALLED_APPS = BASE_APPS + MY_APPS

THIRD_PARTY = [
    "django_countries",
    "django_harlequin",
]
