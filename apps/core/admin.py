from django.contrib import admin
from apps.core.models import OperationLog


class OperationLogAdmin(admin.ModelAdmin):
    model = OperationLog

    fieldsets = [
        ('Operation',
            {'fields': [['time', 'operation']]}),

        ('Object',
            {'fields': [['obj_pk', 'obj_module', 'obj_class']]}),
    ]

    list_display = ('time', 'operation', 'obj_module', 'obj_class')


admin.site.register(OperationLog, OperationLogAdmin)
