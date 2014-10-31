from time import sleep
from datetimewidget.widgets import DateWidget
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
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

    form_class = modelform_factory(Person, widgets={
        "birth": DateWidget(
            options={
                'format': 'yyyy-mm-dd',
                'clearBtn': 'false'
            },
            bootstrap_version=3
        )
    })

    def get_object(self):
        # lets take additional 5000$
        # for optimization work in future
        if self.request.is_ajax():
            sleep(4)

        person = Person.objects.first()
        if not person:
            raise Http404
        return person
