from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AdminSiteTest(LiveServerTestCase):
    DEFAULT_USERNAME = 'admin'
    DEFAULT_PASSWORD = 'admin'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def login_to_admin(self, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
        self.browser.get(self.live_server_url + '/admin/')

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    def test_admin_site_enabled(self):
        self.browser.get(self.live_server_url + '/admin/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

    def test_can_login_with_default_credentials(self):
        self.login_to_admin()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

    def test_person_added_to_admin(self):
        """
            Person model should be added to the admin site.
        """
        self.login_to_admin()

        person_links = self.browser.find_elements_by_css_selector("[href*='admin/person']")
        self.assertTrue(len(person_links) > 0)