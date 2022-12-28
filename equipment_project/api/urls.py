from api.views import (
    DestinationViewSet,
    EquipmentViewSet,
    MovementViewSet,
    UserViewSet,
)
from django.urls import (
    include,
    path,
)
from rest_framework import (
    routers,
)

router = routers.DefaultRouter()

router.register(
    'equipments',
    EquipmentViewSet,
    basename='equipment-list'
)
router.register(
    'movements',
    MovementViewSet,
    basename='movement-list'
)

router.register(
    'destinations',
    DestinationViewSet,
    basename='destination-list'
)

router.register(
    'users',
    UserViewSet
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
]
