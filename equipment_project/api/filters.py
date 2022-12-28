import django_filters
from django.db.models import (
    F,
    Max,
)
from equipments.models import (
    Equipment,
)


class EquipmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name'
    )
    inventory = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='inventory'
    )
    model = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='model'
    )
    nomenclature_key = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='nomenclature_key'
    )
    movement = django_filters.CharFilter(
        method='movement_filter',
        field_name='last_movement'
    )

    class Meta:
        model = Equipment
        fields = (
            'name',
            'inventory',
            'model',
            'nomenclature_key',
            'movement'
        )

    @staticmethod
    def movement_filter(queryset, name, value):
        return queryset.annotate(
            date=Max('movements__date')
        ).filter(
            movements__destination__address__icontains=value,
            movements__date=F('date')
        )
