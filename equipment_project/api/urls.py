from api.views import (
    AttestationViewSet,
    CalibrationViewSet,
    EquipmentViewSet,
    MovementViewSet,
    RentViewSet,
    UserViewSet,
)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(
    'equipments',
    EquipmentViewSet,
    basename='equipment-list'
)
router.register(
    'calibrations',
    CalibrationViewSet,
    basename='calibration-list'
)
router.register(
    'movements',
    MovementViewSet,
    basename='movement-list'
)
router.register(
    'attestations',
    AttestationViewSet,
    basename='attestation-list'
)
router.register(
    'rents',
    RentViewSet,
    basename='rent-list'
)

router.register(
    'users',
    UserViewSet
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
