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

        self.assertIn(person.name, body.text)
        self.assertIn(person.surname, body.text)
        self.assertIn(person.email, body.text)
        self.assertIn(person.jabber, body.text)
        self.assertIn(person.skype, body.text)

        birth_date = person.birth.strftime('%b. %d, %Y')
        self.assertIn(birth_date, body.text)

        for entry in person.bio.split('\r\n'):
            self.assertIn(entry, body.text)

        for entry in person.contacts.split('\r\n'):
            self.assertIn(entry, body.text)
