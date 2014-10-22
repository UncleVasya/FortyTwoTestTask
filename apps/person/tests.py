from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.person.models import Person


class IndexViewTests(TestCase):

    def setUp(self):
        super(IndexViewTests, self).setUp()
        self.person1 = Person.objects.all()[0]
        self.person2 = Person.objects.all()[1]

    def test_index_404(self):
        """
            If there is no persons in DB
            we should get 404 in response.
        """
        Person.objects.all().delete()
        resp = self.client.get(reverse('person:index'))
        self.assertEqual(resp.status_code, 404)

    def test_index_success(self):
        """
            If persons table is not empty
            we should get first Person in response
        """
        resp = self.client.get(reverse('person:index'))

        # check if we have person in response
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('person' in resp.context)

        # check if person is correct
        person = resp.context['person']
        self.assertEqual(person, self.person1)

    def test_index_success_after_removal(self):
        """
            If first person is removed from DB
            we should get next first Person in response
        """
        Person.objects.first().delete()
        resp = self.client.get(reverse('person:index'))

        # check if we have person in response
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('person' in resp.context)

        # check if person is correct
        person = resp.context['person']
        self.assertEqual(person, self.person2)