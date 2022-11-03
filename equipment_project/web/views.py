from core.templatetags.wrappers import is_staff_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from equipments.models import Equipment
from web.forms import (AttestationForm, CalibrationForm, EquipmentForm,
                       MovementForm, RentForm)
from web.utils import (pagination, table_filters,
                       valid_equipment_additional_parameter_saver,
                       valid_form_saver)


@login_required(login_url='users:login')
@is_staff_user
def index(request):
    equipments = table_filters(
        request,
        Equipment.objects.select_related(
            'creator'
        ).prefetch_related(
            'rents',
            'attestations',
            'calibrations',
            'movements'
        ).all()
    )
    page_obj = pagination(equipments, request)
    context = {
        'page_obj': page_obj,
        'title_text': 'Список оборудования'
    }
    return render(request, 'equipments/index.html', context)


@login_required(login_url='users:login')
@is_staff_user
def equipment_get(request, equipment_id):
    equipments = Equipment.objects.filter(pk=equipment_id).select_related(
        'creator'
    ).prefetch_related(
        'rents',
        'attestations',
        'calibrations',
        'movements'
    )
    page_obj = pagination(equipments, request)
    context = {
        'page_obj': page_obj,
        'title_text': 'Добавленное оборудование'
    }
    return render(request, 'equipments/index.html', context)


@login_required(login_url='users:login')
@is_staff_user
def equipment_create(request):
    form = EquipmentForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        return valid_form_saver(form, request)
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )


@login_required(login_url='users:login')
@is_staff_user
def equipment_edit(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    form = EquipmentForm(
        request.POST or None,
        files=request.FILES or None,
        instance=equipment
    )
    if form.is_valid():
        return valid_form_saver(form, request)
    return render(
        request,
        'equipments/create_form.html',
        {'form': form, 'is_edit': True}
    )


@login_required(login_url='users:login')
@is_staff_user
def rent_create(request, equipment_id):
    form = RentForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        return valid_equipment_additional_parameter_saver(
            form,
            equipment_id,
            request,
            'web:attestation_create'
        )
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )


@login_required(login_url='users:login')
@is_staff_user
def attestation_create(request, equipment_id):
    form = AttestationForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        return valid_equipment_additional_parameter_saver(
            form,
            equipment_id,
            request,
            'web:calibration_create'
        )
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )


@login_required(login_url='users:login')
@is_staff_user
def calibration_create(request, equipment_id):
    form = CalibrationForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        return valid_equipment_additional_parameter_saver(
            form,
            equipment_id,
            request,
            'web:movement_create'
        )
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )


@login_required(login_url='users:login')
@is_staff_user
def movement_create(request, equipment_id):
    form = MovementForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        return valid_equipment_additional_parameter_saver(
            form,
            equipment_id,
            request
        )
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )
