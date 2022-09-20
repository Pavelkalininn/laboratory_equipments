from django.core.paginator import Paginator

COUNT_OF_EQUIPMENT = 100
SIMPLE_FILTERED_FIELDS = {
    'equipment_id': 'id',
    'inventory': 'inventory__icontains',
    'name': 'name__icontains',
    'type': 'type__icontains',
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


def pagination(posts, request):
    paginator = Paginator(posts, COUNT_OF_EQUIPMENT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def table_filters(request, equipments):
    for key, value in SIMPLE_FILTERED_FIELDS.items():
        filter_parameter = request.GET.get(key)
        if filter_parameter:
            equipments = equipments.filter(**{value: filter_parameter})

    for key, value in MULTI_FILTERED_FIELDS.items():
        filter_parameter = request.GET.get(key)
        if filter_parameter:
            last_ids = []
            for equip in equipments:
                if getattr(equip, key + 's').first():
                    last_ids.append(
                        getattr(
                            equip,
                            key + 's'
                        ).first().id
                    )
            equipments = equipments.filter(**{
                key + 's__id__in': last_ids,
                value: filter_parameter}
            )
    return equipments
