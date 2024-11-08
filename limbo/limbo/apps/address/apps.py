from django.apps import AppConfig


class AddressConfig(AppConfig):
    name = "limbo.apps.address"
    verbose_name = "Address"

    def ready(self):
        from . import signals  # noqa
