from django.views import generic
from apps.requestlog.models import RequestLog


class RequestsView(generic.ListView):
    REQUESTS_TO_SHOW = 10

    def get_queryset(self):
        requests = RequestLog.objects.all()
        return requests[:self.REQUESTS_TO_SHOW]
