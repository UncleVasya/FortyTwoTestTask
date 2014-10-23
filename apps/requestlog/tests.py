from itertools import cycle
import datetime


from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from apps.requestlog.models import RequestLog


class RequestLoggingTests(TestCase):
    REQUEST_URLS = (
        reverse('admin:index'),
        '/SOME/WRONG/URL',
    )
    REQUESTS_TO_SHOW = 10
    REQUESTS_TO_MAKE = REQUESTS_TO_SHOW * 3

    requests_done = []

    def setUp(self):
        super(RequestLoggingTests, self).setUp()
        RequestLog.objects.all().delete()
        # make some requests and remember them
        urls = cycle(self.REQUEST_URLS)
        for _ in range(self.REQUESTS_TO_MAKE):
            path = urls.next()
            req = RequestFactory().get(path)
            resp = self.client.get(path)
            self.requests_done.append({'request': req, 'response_code': resp.status_code})

    def tearDown(self):
        RequestLog.objects.all().delete()
        self.requests_done = []

    def test_all_requests_are_logged(self):
        """
            Amount of logged requests should match
            the number of requests we made.

            Logged data should match the real data
            of executed requests (including order)
        """
        request_logs = RequestLog.objects.all()
        self.assertEqual(self.REQUESTS_TO_MAKE,
                         request_logs.count())
        # check logs data
        for request_log, real_data in zip(request_logs, self.requests_done):
            real_request = real_data['request']
            real_response = real_data['response_code']

            self.assertEqual(request_log.path,          real_request.path)
            self.assertEqual(request_log.method,        real_request.method)
            self.assertEqual(request_log.address,       real_request.get_host())
            self.assertEqual(request_log.query,         real_request.META['QUERY_STRING'])
            self.assertEqual(request_log.response_code, real_response)

            self.assertIsInstance(request_log.time_start, datetime.datetime)
            self.assertIsInstance(request_log.time_end,   datetime.datetime)
