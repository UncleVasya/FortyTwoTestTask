from StringIO import StringIO
from django.core.management import call_command, CommandError
from django.test import TestCase


class PrintModelsTest(TestCase):

    def test_command_accepts_no_args(self):
        """
            Command should not accept any args.
        """
        with self.assertRaises(CommandError):
            call_command('print_models', ['blabla'])

    def test_command_output(self):
        """
            Command output should contain data
            about project models.
        """
        default_models = ('ContentType', 'Permission', 'Session')

        out, err = StringIO(), StringIO()
        call_command('print_models', stdout=out, stderr=err)

        out.seek(0), err.seek(0)
        out, err = str(out.read()), str(err.read())

        self.assertTrue(all(model in out for model in default_models))
        self.assertTrue(all(model in err for model in default_models))
