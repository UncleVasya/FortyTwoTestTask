from django.http import Http404
from django.views import generic
from apps.person.models import Person


class IndexView(generic.DetailView):
    def get_object(self):
        person = Person.objects.first()
        if not person:
            raise Http404
        return person
