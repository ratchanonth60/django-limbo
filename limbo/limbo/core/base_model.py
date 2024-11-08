from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="updated_%(class)s_set",
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="created_%(class)s_set",
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Base")
        abstract = True
