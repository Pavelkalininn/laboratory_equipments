import django_filters
from equipments.models import Equipment


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
    type = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='type'
    )

    class Meta:
        model = Equipment
        fields = ('name', 'inventory', 'model', 'type')
