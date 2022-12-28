COUNT_OF_EQUIPMENT = 100
SIMPLE_FILTERED_FIELDS = {
    'equipment_id': 'id',
    'inventory': 'inventory__icontains',
    'name': 'name__icontains',
    'model': 'model__icontains',
    'without_address': 'movements__destination__isnull'
}

MULTI_FILTERED_FIELDS = {
    'movement': 'movements__destination__address__icontains'
}
