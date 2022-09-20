from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.templatetags.wrappers import is_staff_user
from equipments.models import Equipment
from web.forms import (AttestationForm, CalibrationForm, EquipmentForm,
                       MovementForm, RentForm)
from web.utils import pagination


@login_required(login_url='users:login')
@is_staff_user
def index(request):
    equipments = Equipment.objects.select_related(
        'creator'
    ).prefetch_related(
        'rents',
        'attestations',
        'calibrations',
        'movements'
    ).all()
    equipment_id = request.GET.get('equipment_id')
    inventory = request.GET.get('inventory')
    name = request.GET.get('name')
    type = request.GET.get('type')
    model = request.GET.get('model')
    documents = request.GET.get('documents')
    manufacturer = request.GET.get('manufacturer')
    rent = request.GET.get('rent')
    attestation = request.GET.get('attestation')
    calibration = request.GET.get('calibration')
    movement = request.GET.get('movement')

    if equipment_id:
        equipments = equipments.filter(id=equipment_id)
    if inventory:
        equipments = equipments.filter(inventory__icontains=inventory)
    if name:
        equipments = equipments.filter(name__icontains=name)
    if type:
        equipments = equipments.filter(type__icontains=type)
    if model:
        equipments = equipments.filter(model__icontains=model)
    if documents:
        equipments = equipments.filter(documents__name__icontains=documents)
    if manufacturer:
        equipments = equipments.filter(manufacturer__icontains=manufacturer)
    if rent:
        last_rents_ids = []
        for equip in equipments:
            if equip.rents.first():
                last_rents_ids.append(equip.rents.all()[0].id)
        equipments = equipments.filter(
            id__in=last_rents_ids,
            rents__renter__name__icontains=rent
        )
    if attestation:
        last_attestations_ids = []
        for equip in equipments:
            if equip.attestations.last():
                last_attestations_ids.append(equip.attestations.last().id)
        equipments = equipments.filter(
            id__in=last_attestations_ids,
            attestations__name__icontains=attestation
        )
    if calibration:
        last_calibrations_ids = []
        for equip in equipments:
            if equip.calibrations.last():
                last_calibrations_ids.append(equip.calibrations.last().id)
        equipments = equipments.filter(
            id__in=last_calibrations_ids,
            calibrations__name__icontains=calibration
        )
    if movement:
        last_movements_ids = []
        for equip in equipments:
            if equip.movements.last():
                last_movements_ids.append(equip.movements.last().id)
        equipments = equipments.filter(
            id__in=last_movements_ids,
            movements__destination__address__icontains=movement
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
    equipments = Equipment.objects.filter(id=equipment_id).select_related(
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
        new_form = form.save(commit=False)
        new_form.creator = request.user
        equipment = form.save()
        if 'create_and_exit' in request.POST:
            return redirect('web:equipment_get', equipment.pk)
        return redirect('web:rent_create', equipment.pk)
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
        )


@login_required(login_url='users:login')
@is_staff_user
def equipment_edit(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    form = EquipmentForm(
        request.POST or None,
        files=request.FILES or None,
        instance=equipment
    )
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.creator = request.user
        form.save()
        if 'create_and_exit' in request.POST:
            return redirect('web:equipment_get', equipment.pk)
        return redirect('web:rent_create', equipment.pk)
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
        new_form = form.save(commit=False)
        new_form.equipment = get_object_or_404(Equipment, id=equipment_id)
        new_form.creator = request.user
        new_form.save()
        if 'create_and_exit' in request.POST:
            return redirect('web:equipment_get', equipment_id)
        return redirect('web:attestation_create', equipment_id)
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
        form.creator = request.user
        new_form = form.save(commit=False)
        new_form.equipment = get_object_or_404(Equipment, id=equipment_id)
        new_form.creator = request.user
        new_form.save()
        if 'create_and_exit' in request.POST:
            return redirect('web:equipment_get', equipment_id)
        return redirect('web:calibration_create', equipment_id)
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
        form.creator = request.user
        new_form = form.save(commit=False)
        new_form.equipment = get_object_or_404(Equipment, id=equipment_id)
        new_form.creator = request.user
        new_form.save()
        if 'create_and_exit' in request.POST:
            return redirect('web:equipment_get', equipment_id)
        return redirect('web:movement_create', equipment_id)
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
        form.creator = request.user
        new_form = form.save(commit=False)
        new_form.equipment = get_object_or_404(Equipment, id=equipment_id)
        new_form.creator = request.user
        new_form.save()
        return redirect('web:equipment_get', equipment_id)
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
        )
