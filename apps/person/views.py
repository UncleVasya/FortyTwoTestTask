from django.views import generic
from apps.person.models import Person


class IndexView(generic.DetailView):
    model = Person

    def get_object(self):
        pass
