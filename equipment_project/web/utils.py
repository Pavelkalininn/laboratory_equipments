from typing import Union

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from equipments.models import Equipment
from web.const import (COUNT_OF_EQUIPMENT, MULTI_FILTERED_FIELDS,
                       SIMPLE_FILTERED_FIELDS)
from web.forms import (AttestationForm, CalibrationForm, EquipmentForm,
                       MovementForm, RentForm)


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
                if getattr(equip, f'{key}s').first():
                    last_ids.append(
                        getattr(
                            equip,
                            f'{key}s'
                        ).first().id
                    )
            equipments = equipments.filter(
                **{f'{key}s__id__in': last_ids,
                   value: filter_parameter
                   }
            )
    return equipments


def valid_form_saver(form: EquipmentForm, request):
    new_form = form.save(commit=False)
    new_form.creator = request.user
    equipment = form.save()
    if 'create_and_exit' in request.POST:
        return redirect('web:equipment_get', equipment.pk)
    return redirect('web:rent_create', equipment.pk)


def valid_equipment_additional_parameter_saver(
        form: Union[RentForm, AttestationForm, CalibrationForm, MovementForm],
        equipment_id: int,
        request,
        next_redirect_url: str = None
):
    new_form = form.save(commit=False)
    new_form.equipment = get_object_or_404(Equipment, pk=equipment_id)
    new_form.creator = request.user
    new_form.save()
    if not next_redirect_url or 'create_and_exit' in request.POST:
        return redirect('web:equipment_get', equipment_id)
    return redirect(next_redirect_url, equipment_id)
