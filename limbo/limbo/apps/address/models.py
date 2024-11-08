from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from limbo.core.base_model import BaseModel

from .constants import TITLE_CHOICES


class Address(BaseModel):
    title = models.CharField(
        pgettext_lazy("Treatment Pronouns for the customer", "Title"),
        max_length=64,
        choices=TITLE_CHOICES,
        blank=True,
    )
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    line1 = models.CharField(_("First line of address"), max_length=255)
    line2 = models.CharField(_("Second line of address"), max_length=255, blank=True)
    country = CountryField(
        _("Country"),
        blank_label="Select Country",
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=20,
        blank=True,
    )

    phone_number = PhoneNumberField(_("Phone Number"), null=True, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    state = models.CharField(_("State/Province"), max_length=255, blank=True)

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.state}, {self.country}"

    def flag_url(self, size=48):
        """
        Generates the URL for the country's flag image.

        Args:
            size (int): Size of the flag image (default is 48).

        Returns:
            str: URL of the flag image.
        """
        if not self.country:
            return ""
        return f"https://flagsapi.com/{self.country.code.upper()}/flat/{size}.png"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
