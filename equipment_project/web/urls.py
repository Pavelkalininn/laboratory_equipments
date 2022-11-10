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
        'rent_create/<int:equipment_id>/',
        views.rent_create,
        name='rent_create'
    ),
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
        'attestation_create/<int:equipment_id>/',
        views.attestation_create,
        name='attestation_create'
    ),
    path(
        'calibration_create/<int:equipment_id>/',
        views.calibration_create,
        name='calibration_create'
    ),
    path(
        'movement_create/<int:equipment_id>/',
        views.movement_create,
        name='movement_create'
    ),
]
