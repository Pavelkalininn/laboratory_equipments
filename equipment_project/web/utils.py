import datetime
from typing import (
    List,
)

from django.contrib.auth import (
    get_user_model,
)
from django.core.paginator import (
    Paginator,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from equipments.models import (
    Equipment,
    Movement,
)
from web.const import (
    COUNT_OF_EQUIPMENT,
    MULTI_FILTERED_FIELDS,
    SIMPLE_FILTERED_FIELDS,
)
from web.forms import (
    EquipmentForm,
    MovementCreateForm,
)

User = get_user_model()


def pagination(equipments, request):
    paginator = Paginator(equipments, COUNT_OF_EQUIPMENT)
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
    return equipments.distinct()


def valid_form_saver(form: EquipmentForm, request):
    new_form = form.save(commit=False)
    new_form.creator = request.user
    equipment = form.save()
    return redirect('web:movement_create', equipment.pk)


def valid_equipment_additional_parameter_saver(
        form: MovementCreateForm,
        equipment_ids: List[int],
        request,
        next_redirect_url: str = None
):
    today = datetime.date.today()
    data = form.cleaned_data
    current_date = data.get('date')
    data['date'] = current_date if current_date else today
    data['early'] = current_date < today if current_date else False
    data['late'] = current_date > today if current_date else False
    movements = []
    for current_id in equipment_ids:
        movements.append(
            Movement(
                **data,
                equipment=get_object_or_404(Equipment, pk=current_id),
                creator=request.user
            )
        )
    Movement.objects.bulk_create(movements)
    return redirect('web:index')
