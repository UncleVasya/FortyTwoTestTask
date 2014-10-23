from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from apps.person.models import Person
from apps.requestlog.models import RequestLog


class RequestsPageTest(LiveServerTestCase):
    MAX_REQUESTS_TO_SHOW = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_requests_render(self):
        """
            Rendered page should contain
            correct amount of requests shown.

            Shown requests must be the first requests from DB
            (in the same order).
        """
        requests_in_db = RequestLog.objects.all()
        num_requests_in_db = requests_in_db.count()

        self.browser.get(self.live_server_url + reverse('requestlog:requests'))
        body = self.browser.find_element_by_tag_name('body')

        requests_on_page = body.find_elements_by_class_name('request')

        # check shown requests amount is correct
        num_requests_to_show = min(self.MAX_REQUESTS_TO_SHOW, num_requests_in_db + 1)
        self.assertEqual(num_requests_to_show,
                         len(requests_on_page))

        # check that requests on page are the first ones from DB
        id_fields = body.find_elements_by_class_name('request_id')
        for i, id_field in enumerate(id_fields):
            self.assertEqual(int(id_field.text),
                             requests_in_db[i].pk)
