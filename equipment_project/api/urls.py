from api.views import (AttestationViewSet, CalibrationViewSet,
                       EquipmentViewSet, MovementViewSet, RentViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(
    '(?P<telegram_id>[0-9]+)/equipments',
    EquipmentViewSet,
    basename='equipment-list'
)
router.register(
    '(?P<telegram_id>[0-9]+)/calibrations',
    CalibrationViewSet,
    basename='calibration-list'
)
router.register(
    '(?P<telegram_id>[0-9]+)/movements',
    MovementViewSet,
    basename='movement-list'
)
router.register(
    '(?P<telegram_id>[0-9]+)/attestations',
    AttestationViewSet,
    basename='attestation-list'
)
router.register(
    '(?P<telegram_id>[0-9]+)/rents',
    RentViewSet,
    basename='rent-list'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
