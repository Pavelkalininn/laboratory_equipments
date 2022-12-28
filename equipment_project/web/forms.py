from django import (
    forms,
)
from django.core.exceptions import (
    ValidationError,
)
from django.db.models import (
    Q,
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
    date = forms.DateField(
        required=False
    )

    def validate(self, obj):
        super().validate(obj)
        request = self.context.get('request')
        if Equipment.objects.filter(
                (Q(pk__in=request.GET.getlist('ids')) | Q(
                    pk=request.kwargs.get('equipment_id'))),
                movements__destination=None
        ).exists():
            raise ValidationError(
                'Invalid value: %(value)s',
                code='invalid',
                params={'value': '42'},
            )

    class Meta:
        model = Movement
        fields = (
            'date',
            'recipient',
        )


class MovementUpdateForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('destination',)
