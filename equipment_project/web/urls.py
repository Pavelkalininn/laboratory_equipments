from django.urls import (
    path,
)
from web import (
    views,
)

app_name = "web"

urlpatterns = [
    path('', views.index, name="index"),
    path(
        'equipment_get/<int:equipment_id>/',
        views.equipment_get,
        name='equipment_get'
    ),
    path(
        'equipment_create/',
        views.equipment_create,
        name='equipment_create'
    ),
    path(
        'equipment_edit/<int:equipment_id>/',
        views.equipment_edit,
        name='equipment_edit'
    ),
    path(
        'movement_create/<int:equipment_id>/',
        views.movement_create,
        name='movement_create'
    ),
    path(
        'movement_update/<int:movement_id>/',
        views.movement_update,
        name='movement_update'
    ),
    path(
        'manual_download/<int:equipment_id>/',
        views.manual_download,
        name='manual_download'
    ),
    path(
        'my_equipments/',
        views.my_equipments,
        name='my_equipments'
    )
]
