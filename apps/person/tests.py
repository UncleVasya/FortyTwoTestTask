from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.person.models import Person


class IndexViewTests(TestCase):

    def check_person_render(self, person, content):
        """
            Helper function to check rendered html
            for correct person data
        """
        # check that only one person is shown
        self.assertEqual(1, content.count('id="label_name"'))
        self.assertEqual(1, content.count('id="label_surname"'))
        self.assertEqual(1, content.count('id="label_birth"'))
        self.assertEqual(1, content.count('id="label_bio"'))
        self.assertEqual(1, content.count('id="label_email"'))
        self.assertEqual(1, content.count('id="label_jabber"'))
        self.assertEqual(1, content.count('id="label_skype"'))
        self.assertEqual(1, content.count('id="label_contacts"'))

        # check that person data is correct
        self.assertIn(person.name, content)
        self.assertIn(person.surname, content)
        self.assertIn(person.email, content)
        self.assertIn(person.jabber, content)
        self.assertIn(person.skype, content)

        birth_date = person.birth.strftime('%b. %d, %Y')
        self.assertIn(birth_date, content)

        for entry in person.bio.split('\r\n'):
            self.assertIn(entry, content)

        for entry in person.contacts.split('\r\n'):
            self.assertIn(entry, content)

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

        # check html template
        self.assertTemplateUsed(resp, 'person/person_detail.html')
        self.check_person_render(person, resp.content)

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

        # check html template
        self.assertTemplateUsed(resp, 'person/person_detail.html')
        self.check_person_render(person, resp.content)
