from django.contrib import admin

from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'inventory',
        'name',
        'type',
        'model',
        'manufacturer',
        'nomenclature_key',
        'document_path'

    )

    empty_value_display = '-пусто-'


class RentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'renter',
        'date',
        'equipment'

    )


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Document)
admin.site.register(Destination)
admin.site.register(Movement)
admin.site.register(Rent, RentAdmin)
admin.site.register(Attestation)
admin.site.register(Calibration)
admin.site.register(Organization)
