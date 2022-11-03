COUNT_OF_EQUIPMENT = 100
SIMPLE_FILTERED_FIELDS = {
    'equipment_id': 'id',
    'inventory': 'inventory__icontains',
    'name': 'name__icontains',
    'serial_number': 'serial_number__icontains',
    'model': 'model__icontains',
    'documents': 'documents__name__icontains',
    'manufacturer': 'manufacturer__icontains'
}

MULTI_FILTERED_FIELDS = {
    'rent': 'rents__renter__name__icontains',
    'attestation': 'attestations__name__icontains',
    'calibration': 'calibrations__name__icontains',
    'movement': 'movements__destination__address__icontains'
}