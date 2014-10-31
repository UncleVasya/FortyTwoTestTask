import json
import os
from PIL import Image
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.datetime_safe import date
import apps
from apps.person.models import Person


def is_person_shown(person, content):
    """
        Helper function to check if rendered html
        contains data about specific person
    """
    fields = [
        person.name,
        person.surname,
        person.email,
        person.jabber,
        person.skype,
        person.birth.strftime('%Y-%m-%d')
    ] + person.bio.split('\r\n') + \
        person.contacts.split('\r\n')

    return all(entry in content for entry in fields)


class IndexViewTests(TestCase):
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
        self.assertTrue(is_person_shown(person, resp.content))
        self.assertFalse(is_person_shown(self.person2, resp.content))

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
        self.assertTrue(is_person_shown(person, resp.content))
        self.assertFalse(is_person_shown(self.person1, resp.content))


class UpdateViewTests(TestCase):
    UPDATE_URL = reverse('person:person_update')
    LOGIN_REDIRECT_URL = reverse('login') + '?next=' + UPDATE_URL
    SUCCESS_REDIRECT_URL = reverse('person:index')

    def setUp(self):
        self.new_data = {
            'name': 'Jane',
            'surname': 'Doe',
            'birth': date(1980, 7, 2),
            'bio': 'I am a person for test',
            'email': 'jane.doe@gmail.com',
            'jabber': 'jane.doe@jabber.com',
            'skype': 'jane_doe',
            'contacts': 'Nope'
        }

        self.client.login(
            username='admin',
            password='admin'
        )

        self.person1 = Person.objects.all()[0]
        self.person2 = Person.objects.all()[1]

    def tearDown(self):
        self.client.logout()

    def test_get_update_page(self):
        resp = self.client.get(self.UPDATE_URL)

        self.assertTrue(is_person_shown(self.person1, resp.content))
        self.assertFalse(is_person_shown(self.person2, resp.content))

    def test_update_with_valid_data(self):
        """
            Person in DB should be updated with new values.

            User should be redirected to the index page
        """
        resp = self.client.post(self.UPDATE_URL, self.new_data)

        self.assertTrue(match_person(Person.objects.first(),
                                     self.new_data))
        self.assertRedirects(resp, self.SUCCESS_REDIRECT_URL)

    def test_update_with_invalid_birth(self):
        """
            If entered birth date is invalid,
            user should see update page again
            with error message.
        """
        self.new_data['birth'] = 'bla-bla-bla'
        resp = self.client.post(self.UPDATE_URL, self.new_data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('birth' in resp.context['form'].errors)

    def test_update_with_invalid_email(self):
        """
            If entered email is invalid,
            user should see update page again
            with error message.
        """
        self.new_data['email'] = 'bla-bla-bla'
        resp = self.client.post(self.UPDATE_URL, self.new_data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('email' in resp.context['form'].errors)

    def test_update_with_invalid_jabber(self):
        """
            If entered jabber is invalid,
            user should see update page again
            with error message.
        """
        self.new_data['jabber'] = 'bla-bla-bla'
        resp = self.client.post(self.UPDATE_URL, self.new_data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('jabber' in resp.context['form'].errors)

    def test_anonymous_access_denied(self):
        """
            Anonymous should not be able to GET update page.

            Anonymous should not be able to update user via POST
            (data in DB should not be changed).

            Anonymous should be redirected to the login page.
        """
        self.client.logout()

        resp = self.client.get(self.UPDATE_URL)
        self.assertRedirects(resp, self.LOGIN_REDIRECT_URL)

        old_person = Person.objects.first()
        resp = self.client.post(self.UPDATE_URL, self.new_data)
        new_person = Person.objects.first()
        self.assertEqual(old_person.name, new_person.name)
        self.assertRedirects(resp, self.LOGIN_REDIRECT_URL)

    def test_update_with_valid_photo(self):
        """
            Person photo should be updated.

            User should be redirected to the index page.
        """
        person = Person.objects.first()

        app_dir = os.path.abspath(apps.person.__path__[0])
        photo_path = os.path.join(app_dir, 'test_media/photo.jpg')
        with open(photo_path) as photo:
            self.new_data['photo'] = photo

            resp = self.client.post(self.UPDATE_URL, self.new_data)
            self.assertRedirects(resp, self.SUCCESS_REDIRECT_URL)

            updated_person = Person.objects.first()
            self.assertNotEqual(person.photo, updated_person.photo)

            # check that photo was resized on server side
            original = Image.open(photo_path)
            saved = Image.open(updated_person.photo.path)
            self.assertNotEqual(original.size, saved.size)

            os.remove(updated_person.photo.path)

    def test_update_with_invalid_photo(self):
        """
            User should see update page again
            with corresponding error.
        """
        app_dir = os.path.abspath(apps.person.__path__[0])
        with open(os.path.join(app_dir, 'test_media/incorrect_photo.jpg')) as photo:
            self.new_data['photo'] = photo

            resp = self.client.post(self.UPDATE_URL, self.new_data)

            self.assertEqual(resp.status_code, 200)
            self.assertTrue('photo' in resp.context['form'].errors)

    def test_ajax_update_with_valid_data(self):
        """
            Person in DB should be updated with new values.

            User should NOT be redirected to the index page.
        """
        resp = self.client.post(self.UPDATE_URL, self.new_data,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertTrue(match_person(Person.objects.first(),
                                     self.new_data))
        self.assertEqual(resp.status_code, 200)

    def test_ajax_update_with_invalid_data(self):
        """
            Response should have code 400.

            Response data should contain form errors.
        """
        self.new_data['name'] = ''
        self.new_data['birth'] = 'bla-bla-bla'

        resp = self.client.post(self.UPDATE_URL, self.new_data,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 400)

        resp = json.loads(resp.content)
        self.assertIn('name', resp['errors'])
        self.assertIn('birth', resp['errors'])


def match_person(person, data):
    return \
        person.name == data['name'] and \
        person.surname == data['surname'] and \
        person.birth == data['birth'] and \
        person.email == data['email'] and \
        person.jabber == data['jabber'] and \
        person.skype == data['skype'] and \
        person.contacts == data['contacts']
