from django.views import generic
from apps.requestlog.models import RequestLog


class RequestsView(generic.ListView):

    def get_queryset(self):
        return RequestLog.objects.all().select_related()
