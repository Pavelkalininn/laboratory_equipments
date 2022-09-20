from api.filters import EquipmentFilter
from api.serializers import (AttestationSerializer, CalibrationSerializer,
                             DestinationSerializer, DocumentSerializer,
                             EquipmentCreateSerializer, EquipmentSerializer,
                             MovementCreateSerializer, MovementSerializer,
                             OrganizationSerializer, RentSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent)
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS


class CalibrationViewSet(viewsets.ModelViewSet):
    queryset = Calibration.objects.all()
    serializer_class = CalibrationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('equipment', 'name')


class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('equipment', 'destination')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MovementSerializer
        return MovementCreateSerializer


class AttestationViewSet(viewsets.ModelViewSet):
    queryset = Attestation.objects.all()
    serializer_class = AttestationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('equipment', 'name')


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('equipment', 'renter', 'owner')


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = EquipmentFilter
    filterset_fields = ('name', 'inventory', 'model', 'type')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return EquipmentSerializer
        return EquipmentCreateSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('name',)


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('address',)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('name', )
