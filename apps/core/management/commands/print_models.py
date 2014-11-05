from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Prints all project models and the count of objects in every model"

    def handle_noargs(self, **options):
        for ct in ContentType.objects.all():
            m = ct.model_class()
            print "%s.%s\t%d" % \
                  (m.__module__, m.__name__, m.objects.all().count())