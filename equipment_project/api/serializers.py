from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent)
from rest_framework import serializers


class DocumentSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Document


class OrganizationSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Organization


class CalibrationSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Calibration


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
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all()
    )
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Movement


class RentSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Rent


class AttestationSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Attestation


class EquipmentCreateSerializer(serializers.ModelSerializer):
    rents = serializers.PrimaryKeyRelatedField(
        queryset=Rent.objects.all(),
        many=True,
        required=False
    )
    attestations = serializers.PrimaryKeyRelatedField(
        queryset=Attestation.objects.all(),
        many=True,
        required=False
    )
    calibrations = serializers.PrimaryKeyRelatedField(
        queryset=Calibration.objects.all(),
        many=True,
        required=False
    )
    movements = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(),
        many=True,
        required=False
    )
    documents = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(),
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
            'inventory', 'name', 'serial_number', 'model', 'manufacturer',
            'nomenclature_key', 'documents', 'document_path',
            'rents', 'attestations', 'calibrations', 'movements', 'creator'
        )
        model = Equipment


class EquipmentSerializer(EquipmentCreateSerializer):
    rents = RentSerializer(many=True)
    attestations = AttestationSerializer(many=True)
    calibrations = CalibrationSerializer(many=True)
    movements = MovementSerializer(many=True)
    documents = DocumentSerializer(many=True)
