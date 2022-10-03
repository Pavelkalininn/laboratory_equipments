from django import forms
from equipments.models import (Attestation, Calibration, Equipment, Movement,
                               Rent)


class RentForm(forms.ModelForm):

    class Meta:
        model = Rent
        fields = ('owner', 'renter', 'date')


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = (
            'inventory',
            'name',
            'serial_number',
            'model',
            'manufacturer',
            'nomenclature_key',
            'documents',
            'document_path',
        )


class AttestationForm(forms.ModelForm):

    class Meta:
        model = Attestation
        fields = ('name', 'validity_period', 'date')


class CalibrationForm(forms.ModelForm):

    class Meta:
        model = Calibration
        fields = ('name', 'validity_period', 'date')


class MovementForm(forms.ModelForm):

    class Meta:
        model = Movement
        fields = ('destination', 'date')
