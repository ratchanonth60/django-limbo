from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from djangoql.admin import DjangoQLSearchMixin


from .forms import AddressAdminForm
from .models import Address


class AddressAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    form = AddressAdminForm
    list_per_page = 10
    list_display = (
        "line1",
        "city",
        "state",
        "country_flag",
        "postal_code",
        "created_at",
    )
    search_fields = ("street_address", "city", "state", "postal_code")
    list_filter = ("country", "state")

    def country_flag(self, obj):
        if obj.country:
            return format_html(
                """<img class="country-select-flag"
                src="{}"
                alt="{} Flag"
                style="margin: auto" />""",
                obj.country.flag,
                obj.country.name,
            )
        return ""

    country_flag.short_description = _("Flag")


admin.site.register(Address, AddressAdmin)
