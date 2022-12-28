from django.contrib import (
    admin,
)
from django.contrib.auth.admin import (
    UserAdmin,
)
from equipments.models import (
    Destination,
    Equipment,
    Movement,
    User,
)

admin.site.empty_value_display = '-пусто-'

UserAdmin.fieldsets += (('Extra Fields', {'fields': ('telegram_id', )}),)


class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'telegram_id'
    )
    search_fields = ('username', 'email', 'first_name')
    list_filter = ('username', 'email', 'first_name', 'telegram_id')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'inventory',
        'name',
        'model',
        'nomenclature_key',
        'document_path'

    )


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Destination)
admin.site.register(Movement)
admin.site.register(User, CustomUserAdmin)
