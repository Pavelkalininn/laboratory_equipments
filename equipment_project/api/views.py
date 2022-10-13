from api.filters import EquipmentFilter
from api.permissions import IsStaff
from api.serializers import (AttestationSerializer, CalibrationSerializer,
                             DestinationSerializer, DocumentSerializer,
                             EquipmentCreateSerializer, EquipmentSerializer,
                             MovementCreateSerializer, MovementSerializer,
                             OrganizationSerializer, RentSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent, User)
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS


class CalibrationViewSet(viewsets.ModelViewSet):
    queryset = Calibration.objects.all()
    serializer_class = CalibrationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('equipment', 'name')

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('equipment', 'destination')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MovementSerializer
        return MovementCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class AttestationViewSet(viewsets.ModelViewSet):
    queryset = Attestation.objects.all()
    serializer_class = AttestationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('equipment', 'name')

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('equipment', 'renter', 'owner')

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_class = EquipmentFilter
    filterset_fields = ('name', 'inventory', 'model', 'serial_number')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return EquipmentSerializer
        return EquipmentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('address',)

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    filterset_fields = ('name', )

    def perform_create(self, serializer):
        serializer.save(
            creator=get_object_or_404(
                User,
                telegram_id=self.request.data.get("telegram_id")
            )
        )
