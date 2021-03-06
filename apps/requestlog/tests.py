from itertools import cycle
import datetime


from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from apps.requestlog.models import RequestLog


class RequestLoggingTests(TestCase):
    REQUEST_URLS = (
        reverse('requestlog:requests'),
        reverse('admin:index'),
        '/SOME/WRONG/URL',
    )
    MAX_REQUESTS_TO_SHOW = 10
    REQUESTS_TO_MAKE = MAX_REQUESTS_TO_SHOW * 3

    requests_done = []

    def check_requests_render(self, request_list, content):
        """
            Helper function to check rendered html
            for correct requests data
        """
        rendered_requests = content.count('request ')
        self.assertEqual(rendered_requests, request_list.count())

        for request in request_list:
            self.assertIn(str(request.id), content)
            self.assertIn(request.path, content)

    def setUp(self):
        super(RequestLoggingTests, self).setUp()
        RequestLog.objects.all().delete()
        # make some requests and remember them
        urls = cycle(self.REQUEST_URLS)
        for n in range(self.REQUESTS_TO_MAKE):
            path = urls.next()
            req = RequestFactory().get(path)
            resp = self.client.get(path)
            RequestLog.objects.all()[n].priority = n % 10
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

            self.assertEqual(request_log.path, real_request.path)
            self.assertEqual(request_log.method, real_request.method)
            self.assertEqual(request_log.address, real_request.get_host())
            self.assertEqual(request_log.query, real_request.META['QUERY_STRING'])
            self.assertEqual(request_log.response_code, real_response)

            self.assertIsInstance(request_log.time_start, datetime.datetime)
            self.assertIsInstance(request_log.time_end, datetime.datetime)

    def test_requests_page_with_full_db(self):
        """
            Amount of objects returned from view
            should match REQUESTS_TO_SHOW value
        """
        resp = self.client.get(reverse('requestlog:requests'))

        # check if we have request list in response
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('requestlog_list' in resp.context)

        # check if requests count is correct
        returned = resp.context['requestlog_list']
        self.assertEqual(self.MAX_REQUESTS_TO_SHOW, returned.count())

        # check if requests are correct
        requests = RequestLog.objects.all().order_by('-priority')
        expected = requests[:self.MAX_REQUESTS_TO_SHOW]
        for request, db_request in zip(returned, expected):
            self.assertEqual(db_request, request)

        # check html render
        self.assertTemplateUsed('requestslog/requestlog_list.html')
        self.check_requests_render(expected, resp.content)

    def test_request_page_with_empty_db(self):
        """
            View should not return error or 404.
            It must return request that was just executed.

            I.e. requests should be logged to DB
            _before_ view processes them.
        """
        RequestLog.objects.all().delete()
        resp = self.client.get(reverse('requestlog:requests'))

        # request above should be logged into DB
        self.assertEqual(1, RequestLog.objects.all().count())

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('requestlog_list' in resp.context)

        returned = resp.context['requestlog_list']
        self.assertEqual(1, returned.count())
        self.assertEqual(RequestLog.objects.first(), returned[0])

        self.assertTemplateUsed('requestlog/requestlog_list.html')
        self.check_requests_render(returned, resp.content)

    def test_request_page_with_almost_empty_db(self):
        """
        if stored requests < REQUESTS_TO_SHOW then
            returned requests = stored requests
        """
        RequestLog.objects.all().delete()

        # make few requests,
        # but less than REQUESTS_TO_SHOW value
        req_count = self.MAX_REQUESTS_TO_SHOW / 2
        for n in range(req_count):
            self.client.get(reverse('admin:index'))
            RequestLog.objects.all()[n].priority = (n % 10) + 1

        resp = self.client.get(reverse('requestlog:requests'))
        req_count += 1

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('requestlog_list' in resp.context)

        returned = resp.context['requestlog_list']
        self.assertEqual(req_count, returned.count())

        self.assertTemplateUsed('requestslog/requestlog_list.html')
        self.check_requests_render(returned, resp.content)

    def test_ajax_update_request(self):
        """
            Request in DB should be updated with new values.
        """
        request = RequestLog.objects.get(pk=13)
        old_priority = request.priority
        new_priority = old_priority + 2

        resp = self.client.post(
            reverse('requestlog:request_update', args=(13,)),
            {'priority': new_priority},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if priority changed in DB
        request = RequestLog.objects.get(pk=13)
        self.assertEqual(request.priority, new_priority)

    def test_ajax_list_request(self):
        """
            Response should contain html table with requests.
        """
        resp = self.client.get(reverse('requestlog:requests'),
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if we have request list in response
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('requestlog_list' in resp.context)

        # check if requests count is correct
        returned = resp.context['requestlog_list']
        self.assertEqual(self.MAX_REQUESTS_TO_SHOW, returned.count())

        # check if requests are correct
        requests = RequestLog.objects.all().order_by('-priority')
        expected = requests[:self.MAX_REQUESTS_TO_SHOW]
        for request, db_request in zip(returned, expected):
            self.assertEqual(request, db_request)

        # check html render
        self.assertTemplateUsed('requestslog/requests_table_body.html')
        self.check_requests_render(expected, resp.content)
