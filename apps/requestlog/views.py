from time import sleep
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.views import generic
from django.views.decorators.http import require_http_methods
from apps.requestlog.mixins import AjaxableResponseMixin
from apps.requestlog.models import RequestLog


class RequestsView(AjaxableResponseMixin, generic.ListView):
    REQUESTS_TO_SHOW = 10

    def get_queryset(self):
        requests = RequestLog.objects.all().order_by('-priority')
        return requests[:self.REQUESTS_TO_SHOW]

    def get_context_data(self, **kwargs):
        context = super(RequestsView, self).get_context_data(**kwargs)
        context['form'] = modelform_factory(RequestLog)
        context['priority_range'] = range(1, 11)
        return context


class RequestUpdateView(generic.UpdateView):
    model = RequestLog
    success_url = reverse_lazy('requestlog:requests')
    form_class = modelform_factory(RequestLog, fields=('priority',))

    def get_object(self):
        # if self.request.is_ajax():
        #     sleep(4)

        return super(RequestUpdateView, self).get_object()