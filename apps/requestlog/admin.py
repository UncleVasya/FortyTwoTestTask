from django.contrib import admin
from apps.requestlog.models import RequestLog


class RequestLogAdmin(admin.ModelAdmin):
    model = RequestLog

    fieldsets = [
        ('Time and result',
            {'fields': [['time_start', 'time_end', 'response_code']]}),

        ('Data',
            {'fields': [['path', 'query', 'method'], 'address']}),
    ]

    list_display = ('time_start', 'path', 'method', 'response_code', 'address')


admin.site.register(RequestLog, RequestLogAdmin)
