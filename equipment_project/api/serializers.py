import datetime

from django.contrib.auth import (
    get_user_model,
)
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from equipments.models import (
    Destination,
    Equipment,
    Movement,
)
from rest_framework import (
    serializers,
)
from rest_framework.relations import (
    StringRelatedField,
)

from equipment_project.settings import (
    TODAY,
)

User = get_user_model()


class DestinationSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Destination


class MovementSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer()
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Movement


class MovementCreateSerializer(serializers.ModelSerializer):
    destination = StringRelatedField()
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('destination', 'date', 'equipment', 'creator')
        model = Movement

    def validate_date(self, value):
        if value in (TODAY, ):
            return datetime.date.today()
        return value


class EquipmentCreateSerializer(serializers.ModelSerializer):

    movements = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(),
        many=True,
        required=False
    )
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'id',
            'inventory',
            'name',
            'model',
            'nomenclature_key',
            'manual',
            'document_path',
            'movements',
            'creator'
        )
        model = Equipment


class EquipmentSerializer(EquipmentCreateSerializer):
    movements = serializers.StringRelatedField(many=True)


class DjoserUserUpdateSerializer(UserSerializer):
    is_staff = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'telegram_id',
            'is_staff'
        )
        model = User

    def get_is_staff(self, obj):
        return obj.is_staff


class DjoserUserCreateSerializer(UserCreateSerializer):
    is_staff = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'telegram_id',
            'is_staff',
            'password'
        )
        model = User

    def get_is_staff(self, obj):
        return obj.is_staff
