from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Address


@receiver(pre_save, sender=Address)
def uppercase_postal_code(sender, instance, **kwargs):
    if instance.postal_code:
        instance.postal_code = instance.postal_code.upper()
