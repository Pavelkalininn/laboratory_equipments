from api.authentication import BotAuthentication
from api.filters import EquipmentFilter
from api.permissions import IsStaff, IsSuperUser
from api.serializers import (AttestationSerializer, CalibrationSerializer,
                             DestinationSerializer, DjoserUserSerializer,
                             DocumentSerializer, EquipmentCreateSerializer,
                             EquipmentSerializer, MovementCreateSerializer,
                             MovementSerializer, OrganizationSerializer,
                             RentSerializer)
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

User = get_user_model()


class CalibrationViewSet(viewsets.ModelViewSet):
    queryset = Calibration.objects.all()
    serializer_class = CalibrationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('equipment', 'name')

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('equipment', 'destination')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MovementSerializer
        return MovementCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class AttestationViewSet(viewsets.ModelViewSet):
    queryset = Attestation.objects.all()
    serializer_class = AttestationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('equipment', 'name')

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('equipment', 'renter', 'owner')

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_class = EquipmentFilter
    filterset_fields = (
        'name',
        'inventory',
        'model',
        'serial_number',
        'nomenclature_key',
        'movement'
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return EquipmentSerializer
        return EquipmentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('address',)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    authentication_classes = [BotAuthentication, ]
    filterset_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class UserViewSet(GenericViewSet, UpdateModelMixin, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = DjoserUserSerializer
    authentication_classes = (BotAuthentication,)

    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        return super().get_authenticators()

    @action(methods=['patch'], detail=False)
    def staff_change(self, request):
        if request.method == 'PATCH':
            new_user = User.objects.get(
                telegram_id=request.data.get("new_user_id")
            )
            is_staff = request.data.get('is_staff')
            new_user.is_staff = is_staff
            serializer = self.get_serializer(
                new_user,
                data={'is_staff': is_staff},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(new_user, '_prefetched_objects_cache', None):
                new_user._prefetched_objects_cache = {}
            return Response(serializer.data)
        raise MethodNotAllowed(method=request.method)

    @action(methods=['get', 'patch', 'put', 'delete'], detail=False)
    def me(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user.username)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH' or request.method == 'PUT':
            partial = True if request.method == 'PATCH' else False
            user = User.objects.get(username=request.user.username)
            data = request.data.copy()
            serializer = self.get_serializer(
                user,
                data=data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(user, '_prefetched_objects_cache', None):
                user._prefetched_objects_cache = {}
            return Response(serializer.data)

        if request.method == 'DELETE':
            raise MethodNotAllowed(method='DELETE')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        if self.request.method == 'POST':
            return (AllowAny(),)
        if self.action == 'me':
            return (IsAuthenticated(),)
        return (IsSuperUser(),)
