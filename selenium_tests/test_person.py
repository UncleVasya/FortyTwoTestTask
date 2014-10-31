from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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


class PersonUpdatePageTest(LiveServerTestCase):
    DEFAULT_USERNAME = 'admin'
    DEFAULT_PASSWORD = 'admin'

    def login(self, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
        self.browser.get(self.live_server_url + reverse('login'))

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.login()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        pass

    def test_datepicker_widget(self):
        """
            User should be able to set birth date
            with calendar widget.
        """
        self.browser.get(self.live_server_url + reverse('person:person_update'))

        birth_field = self.browser.find_element_by_css_selector('input#id_birth')
        datepicker = self.browser.find_element_by_class_name('datetimepicker')

        # at start calendar is hidden
        self.assertFalse(datepicker.is_displayed())

        # calendar pops up on birth field click
        birth_field.click()
        self.assertTrue(datepicker.is_displayed())

        # user picks some date
        dates = datepicker.find_elements_by_class_name('day')
        date = next(date for date in dates if date.text == '13')
        date.click()

        # calendar hides, birth field updated
        self.assertFalse(datepicker.is_displayed())
        formatted_birth = time.strptime(birth_field.get_attribute('value'), '%Y-%m-%d')
        self.assertEqual(formatted_birth.tm_mday, 13)
