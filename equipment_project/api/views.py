import datetime
from http import (
    HTTPStatus,
)

from api.authentication import (
    BotAuthentication,
)
from api.filters import (
    EquipmentFilter,
)
from api.permissions import (
    IsStaff,
    IsSuperUser,
)
from api.serializers import (
    DestinationSerializer,
    DjoserUserCreateSerializer,
    DjoserUserUpdateSerializer,
    EquipmentSerializer,
    MovementCreateSerializer,
    MovementSerializer,
)
from django.contrib.auth import (
    get_user_model,
)
from django.http import (
    FileResponse,
)
from django.shortcuts import (
    get_object_or_404,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from equipments.models import (
    Destination,
    Equipment,
    Movement,
)
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.exceptions import (
    MethodNotAllowed,
)
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from equipment_project.settings import (
    MEDIA_ROOT,
)

User = get_user_model()


class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
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
        data = self.request.data
        destination_address = data.get('destination')
        if not Destination.objects.filter(
                address=destination_address
        ).exists():
            destination = Destination.objects.create(
                address=destination_address
            )
        else:
            destination = get_object_or_404(
                Destination,
                address=destination_address
            )
        equipment = data.get('equipment')
        recipient_last_name = data.get('recipient')

        today = datetime.date.today()
        current_date = datetime.datetime.strptime(
            data.get('date'),
            '%d.%m.%Y'
        ).date()
        date = current_date if current_date else today
        early = current_date < today if current_date else False
        late = current_date > today if current_date else False
        serializer.save(
            creator=self.request.user,
            destination=destination,
            date=date,
            early=early,
            late=late,
            equipment=get_object_or_404(Equipment, pk=equipment),
            recipient=get_object_or_404(User, last_name=recipient_last_name)
        )


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = [IsStaff, ]
    serializer_class = EquipmentSerializer
    authentication_classes = [BotAuthentication, ]
    filterset_class = EquipmentFilter
    filterset_fields = (
        'name',
        'inventory',
        'model',
        'nomenclature_key',
        'movement'
    )

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            creator=self.request.user
        )

    @action(methods=['get'],
            detail=True,
            permission_classes=[IsStaff, ],
            )
    def manual_download(self, request, pk):
        manual = get_object_or_404(Equipment, pk=pk).manual
        filename = str(manual).split('/')[-1]
        return FileResponse(
            open(f'{MEDIA_ROOT}/{manual}', 'rb'),
            status=HTTPStatus.OK,
            as_attachment=True,
            filename=filename
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


class UserViewSet(GenericViewSet, UpdateModelMixin, CreateModelMixin):
    queryset = User.objects.all()
    authentication_classes = (BotAuthentication,)

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return DjoserUserUpdateSerializer
        return DjoserUserCreateSerializer

    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        return super().get_authenticators()

    @action(methods=['patch'], detail=False)
    def staff_change(self, request):
        if request.method == 'PATCH':
            new_user = get_object_or_404(
                User,
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
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH' or request.method == 'PUT':
            partial = True if request.method == 'PATCH' else False
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
