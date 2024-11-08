from django import forms
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import SplitPhoneNumberField

from .models import Address

# You can use a service like FlagsAPI to dynamically display country flags


class AddressAdminForm(forms.ModelForm):
    phone_number = SplitPhoneNumberField(
        required=False,
    )

    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            "country": CountrySelectWidget(
                layout="""{widget}
                <img class="country-select-flag"
                id="{flag_id}" style="margin: auto"
                src="{country.flag}">"""
            )
        }
