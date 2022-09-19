from rest_framework import serializers

from equipments.models import (
    Calibration,
    Movement,
    Equipment,
    Rent,
    Organization,
    Attestation,
    Destination,
    Document
)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Organization


class CalibrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Calibration


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Destination


class MovementSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer()

    class Meta:
        fields = '__all__'
        model = Movement


class MovementCreateSerializer(serializers.ModelSerializer):
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Movement


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Rent


class AttestationSerializer(serializers.ModelSerializer):
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

    class Meta:
        fields = (
            'inventory', 'name', 'type', 'model', 'manufacturer',
            'nomenclature_key', 'documents', 'document_path',
            'rents', 'attestations', 'calibrations', 'movements'
        )
        model = Equipment


class EquipmentSerializer(EquipmentCreateSerializer):
    rents = RentSerializer(many=True)
    attestations = AttestationSerializer(many=True)
    calibrations = CalibrationSerializer(many=True)
    movements = MovementSerializer(many=True)
    documents = DocumentSerializer(many=True)
