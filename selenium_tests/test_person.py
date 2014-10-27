from django.test import LiveServerTestCase
from selenium import webdriver
from apps.person.models import Person


class PersonIndexPageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_person_render(self):
        """
            Rendered page should contain required data
            about first person in DB.
        """
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')

        person = Person.objects.first()
        fields = [
            person.name,
            person.surname,
            person.email,
            person.jabber,
            person.skype,
            person.birth.strftime('%Y-%m-%d')
        ] + person.bio.split('\r\n') + \
            person.contacts.split('\r\n')

        for entry in fields:
            self.assertIn(entry, body.text)

    def test_only_one_person_shown(self):
        """
            Rendered page should contain data
            only for one Person.
        """
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')

        labels = [
            'label_name',
            'label_surname',
            'label_birth',
            'label_bio',
            'label_email',
            'label_jabber',
            'label_skype',
            'label_contacts',
        ]

        for label in labels:
            self.assertEqual(1, len(body.find_elements_by_id(label)))
