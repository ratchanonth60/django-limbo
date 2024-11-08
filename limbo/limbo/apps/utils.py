from django.db.models import Q
from django_filters import rest_framework as filters


class BaseFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    created_by = filters.CharFilter(method="filter_by", field_name="created_by")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")
    updated_by = filters.CharFilter(method="filter_by", field_name="updated_by")
    id = filters.NumberFilter(field_name="id")
    order_by = filters.OrderingFilter(
        fields=(  # เพิ่มการจัดเรียง
            ("created_at", "created_at"),
            ("created_by", "created_by"),
        )
    )

    def filter_by(self, queryset, name, value):
        return queryset.filter(
            Q(updated_by__id__icontains=value)
            | Q(updated_by__username__icontains=value)
        )
