from django.conf import settings
from django.template import RequestContext
from django.test import TestCase, RequestFactory


class SettingsAdderProcessorTests(TestCase):

    def test_settings_are_in_context(self):
        """
            Request context should contain settings object

            Setting in request must be equal to django settings.
        """
        req = RequestFactory().get('')
        ctx = RequestContext(req)

        self.assertTrue('settings' in ctx)
        self.assertEqual(ctx['settings'], settings)
