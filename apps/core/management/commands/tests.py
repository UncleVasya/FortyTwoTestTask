from django.core.management import call_command, CommandError
from django.test import TestCase


class PrintModelsTest(TestCase):

    def test_command_accepts_no_args(self):
        """
            Command should not accept any args
        """
        with self.assertRaises(CommandError):
            call_command('print_models', ['blabla'])


