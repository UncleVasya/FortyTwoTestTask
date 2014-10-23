from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.person.models import Person


class IndexViewTests(TestCase):

    def is_person_shown(self, person, content):
        """
            Helper function to check if rendered html
            contains data about specific person
        """
        result = True
        result = result and (person.name in content)
        result = result and (person.surname in content)
        result = result and (person.email in content)
        result = result and (person.jabber in content)
        result = result and (person.skype in content)

        birth_date = person.birth.strftime('%b. %d, %Y')
        result = result and (birth_date in content)

        for entry in person.bio.split('\r\n'):
            result = result and (entry in content)

        for entry in person.contacts.split('\r\n'):
            result = result and (entry in content)

        return result

    def setUp(self):
        super(IndexViewTests, self).setUp()
        self.person1 = Person.objects.all()[0]
        self.person2 = Person.objects.all()[1]

    def test_index_404(self):
        """
            If there are no persons in DB
            we should get 404 in response.

            Rendered html should use correct template.
        """
        Person.objects.all().delete()

        resp = self.client.get(reverse('person:index'))

        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed(resp, '404.html')

    def test_index_success(self):
        """
            If persons table is not empty
            we should get first Person in response.

            Rendered html should use correct template.
        """
        resp = self.client.get(reverse('person:index'))

        # check if we have person in response
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('person' in resp.context)

        # check if person is correct
        person = resp.context['person']
        self.assertEqual(person, self.person1)

        # check html render
        self.assertTemplateUsed(resp, 'person/person_detail.html')
        self.assertTrue(self.is_person_shown(person, resp.content))
        self.assertFalse(self.is_person_shown(self.person2, resp.content))

    def test_index_success_after_removal(self):
        """
            If first person is removed from DB
            we should get next first Person in response

            Rendered html should use correct template.
        """
        Person.objects.first().delete()
        resp = self.client.get(reverse('person:index'))

        # check if we have person in response
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('person' in resp.context)

        # check if person is correct
        person = resp.context['person']
        self.assertEqual(person, self.person2)

        # check html render
        self.assertTemplateUsed(resp, 'person/person_detail.html')
        self.assertTrue(self.is_person_shown(person, resp.content))
        self.assertFalse(self.is_person_shown(self.person1, resp.content))
