from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic
from apps.person.models import Person


class IndexView(generic.DetailView):
    def get_object(self):
        person = Person.objects.first()
        if not person:
            raise Http404
        return person


class PersonUpdateView(generic.UpdateView):
    success_url = reverse_lazy('person:index')

    def get_object(self):
        person = Person.objects.first()
        if not person:
            raise Http404
        return person
