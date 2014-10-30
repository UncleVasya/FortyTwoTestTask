from time import sleep
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic
from apps.person.mixins import AjaxableUpdateMixin
from apps.person.models import Person


class IndexView(generic.DetailView):
    def get_object(self):
        person = Person.objects.first()
        if not person:
            raise Http404
        return person


class PersonUpdateView(AjaxableUpdateMixin, generic.UpdateView):
    success_url = reverse_lazy('person:index')

    def get_object(self):
        # lets take additional 5000$
        # for optimization work in future
        if self.request.is_ajax():
            sleep(4)

        person = Person.objects.first()
        if not person:
            raise Http404
        return person
