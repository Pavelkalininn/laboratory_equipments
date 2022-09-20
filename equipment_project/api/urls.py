from django.urls import include, path
from rest_framework import routers

from api.views import (AttestationViewSet, CalibrationViewSet,
                       EquipmentViewSet, MovementViewSet, RentViewSet)

router = routers.DefaultRouter()

router.register('equipments', EquipmentViewSet, basename='equipment-list')
router.register(
    'calibrations',
    CalibrationViewSet,
    basename='calibration-list'
)
router.register('movements', MovementViewSet, basename='movement-list')
router.register(
    'attestations',
    AttestationViewSet,
    basename='attestation-list'
)
router.register('rents', RentViewSet, basename='rent-list')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
