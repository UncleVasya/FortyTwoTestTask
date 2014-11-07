from unittest import TestCase
from django.core.urlresolvers import reverse
from django.template import Template, Context
from apps.person.models import Person
from apps.requestlog.models import RequestLog


class EditTagTests(TestCase):

    def test_tag_with_valid_input(self):
        """
            Edit tag should be rendered into
            admin site link for provided object
        """
        person = Person.objects.first()
        request = RequestLog.objects.first()

        html = Template(
            "{% load edit_link %}"
            "{% edit_link person %}"
            "{% edit_link request %}"
        ).render(Context({
            'person': person,
            'request': request
        }))

        self.assertIn(
            reverse('admin:person_person_change', args=(person.id,)),
            html
        )
        self.assertIn(
            reverse('admin:requestlog_requestlog_change', args=(request.id,)),
            html
        )
