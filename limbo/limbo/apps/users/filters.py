from django_filters import rest_framework as filters

from limbo.apps.utils import BaseFilter

from .models import User


class UserFilter(BaseFilter):
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    is_active = filters.BooleanFilter(field_name="is_active")
    is_staff = filters.BooleanFilter(field_name="is_staff")
    date_joined = filters.DateFromToRangeFilter(field_name="date_joined")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
            "created_at",
            "created_by",
        ]
