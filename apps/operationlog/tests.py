from django.test import TestCase
from django.utils.timezone import now
from apps.operationlog.models import OperationLog
from apps.requestlog.models import RequestLog


class OperationLogTest(TestCase):

    def test_object_created(self):
        """
            After object created, DB should contain
            corresponding OperationLog entry.

            Data in the log entry should be correct.
        """
        log_count = OperationLog.objects.count()

        request = RequestLog.objects.create(
            path='some/path',
            method='GET',
            time_start=now(),
            time_end=now(),
            response_code=404,
        )
        log_entry = OperationLog.objects.last()

        # check if new log entry added
        self.assertEqual(OperationLog.objects.count(),
                         log_count + 1)

        # check if log entry is correct
        self.assertEqual(log_entry.operation, 'created')
        self.assertEqual(log_entry.obj_class, RequestLog.__name__)
        self.assertEqual(log_entry.obj_module, RequestLog.__module__)
        self.assertEqual(log_entry.obj_pk, str(request.pk))

    def test_object_updated(self):
        """
            After object updated, DB should contain
            corresponding OperationLog entry.

            Data in the log entry should be correct.
        """
        log_count = OperationLog.objects.count()

        # update some logged request
        request = RequestLog.objects.first()
        request.response = 777
        request.save()

        log_entry = OperationLog.objects.last()

        # check if new log entry added
        self.assertEqual(OperationLog.objects.count(),
                         log_count + 1)

        # check if log entry is correct
        self.assertEqual(log_entry.operation, 'updated')
        self.assertEqual(log_entry.obj_class, RequestLog.__name__)
        self.assertEqual(log_entry.obj_module, RequestLog.__module__)
        self.assertEqual(log_entry.obj_pk, str(request.pk))

    def test_object_deleted(self):
        """
            After object deleted, DB should contain
            corresponding OperationLog entry.

            Data in the log entry should be correct.
        """
        log_count = OperationLog.objects.count()

        # delete some logged request
        request = RequestLog.objects.first()
        request_pk = request.pk
        request.delete()

        log_entry = OperationLog.objects.last()

        # check if new log entry added
        self.assertEqual(OperationLog.objects.count(),
                         log_count + 1)

        # check if log entry is correct
        self.assertEqual(log_entry.operation, 'deleted')
        self.assertEqual(log_entry.obj_class, RequestLog.__name__)
        self.assertEqual(log_entry.obj_module, RequestLog.__module__)
        self.assertEqual(log_entry.obj_pk, str(request_pk))

    def test_log_objects_ignored(self):
        """
            Changes of OperationLog objects
            should NOT be logged in DB.
        """
        log_count = OperationLog.objects.count()

        OperationLog.objects.first().operation = 'blabla'

        self.assertEqual(OperationLog.objects.count(), log_count)
