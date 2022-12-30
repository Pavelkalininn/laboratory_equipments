from http import (
    HTTPStatus,
)

from core.templatetags.wrappers import (
    is_staff_user,
)
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.decorators import (
    login_required,
)
from django.db.models import (
    F,
    Max,
)
from django.http import (
    FileResponse,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from equipments.models import (
    Equipment,
    Movement,
)
from web.forms import (
    EquipmentForm,
    MovementCreateForm,
    MovementUpdateForm,
)
from web.utils import (
    pagination,
    table_filters,
    valid_equipment_additional_parameter_saver,
    valid_form_saver,
)

from equipment_project.settings import (
    MEDIA_ROOT,
)

User = get_user_model()


@login_required(login_url='users:login')
@is_staff_user
def index(request):
    equipments = table_filters(
        request,
        Equipment.objects.select_related(
            'creator'
        ).prefetch_related().all()
    )
    page_obj = pagination(equipments, request)
    context = {
        'page_obj': page_obj,
        'title_text': 'Список оборудования'
    }
    return render(request, 'equipments/index.html', context)


@login_required(login_url='users:login')
@is_staff_user
def my_equipments(request):
    equipments = table_filters(
        request,
        Equipment.objects.annotate(
            last_movement_id=Max('movements__pk')
        ).filter(
            movements__recipient=request.user,
            movements__pk=F('last_movement_id')
        ).distinct().all()
    )
    page_obj = pagination(equipments, request)
    context = {
        'page_obj': page_obj,
        'title_text': 'Список моего оборудования'
    }
    return render(request, 'equipments/index.html', context)


@login_required(login_url='users:login')
@is_staff_user
def equipment_get(request, equipment_id):
    equipment = get_object_or_404(
        Equipment.objects.select_related(
            'creator'
        ).prefetch_related().all(), pk=equipment_id)
    page_obj = pagination((equipment,), request)
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
    equipment = get_object_or_404(
        Equipment.objects.select_related(
            'creator'
        ).prefetch_related().all(), pk=equipment_id)
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
def movement_create(request, equipment_id):
    query_ids = request.GET.getlist('ids')
    equipment_ids = query_ids or [equipment_id, ]
    form = MovementCreateForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        return valid_equipment_additional_parameter_saver(
            form,
            equipment_ids,
            request
        )
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )


@login_required(login_url='users:login')
@is_staff_user
def movement_update(request, movement_id):
    form = MovementUpdateForm(request.POST or None,
                              files=request.FILES or None, )
    if form.is_valid():
        movement = get_object_or_404(Movement, pk=movement_id)
        movement.destination = form.cleaned_data.get('destination')
        movement.save()
        return redirect('web:index')
    return render(
        request,
        'equipments/create_form.html',
        {'form': form}
    )


@login_required(login_url='users:login')
@is_staff_user
def manual_download(request, equipment_id):
    manual = get_object_or_404(Equipment, pk=equipment_id).manual
    filename = str(manual).split('/')[-1]
    return FileResponse(
        open(f'{MEDIA_ROOT}/{manual}', 'rb'),
        status=HTTPStatus.OK,
        as_attachment=True,
        filename=filename
    )
