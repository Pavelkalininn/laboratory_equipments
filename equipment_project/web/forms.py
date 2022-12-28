from django import (
    forms,
)
from equipments.models import (
    Equipment,
    Movement,
)


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = (
            'inventory',
            'name',
            'model',
            'nomenclature_key',
            'manual',
            'document_path',
        )


class MovementCreateForm(forms.ModelForm):

    class Meta:
        model = Movement
        fields = (
            'recipient',
        )


class MovementUpdateForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('destination',)
