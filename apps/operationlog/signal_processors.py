from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from apps.operationlog.models import OperationLog


@receiver(post_save)
def object_saved(sender, instance, created, raw, using, **kwargs):
    if instance.__class__.__name__ in ['OperationLog', 'LogEntry']:
        return

    OperationLog.objects.create(
        time=now(),
        operation='created' if created else 'updated',
        obj_class=instance.__class__.__name__,
        obj_module=instance.__class__.__module__,
        obj_pk=instance.pk
    )


@receiver(post_delete)
def object_deleted(sender, instance, using, **kwargs):
    if instance.__class__.__name__ in ['OperationLog', 'LogEntry']:
        return

    OperationLog.objects.create(
        time = now(),
        operation='deleted',
        obj_class=instance.__class__.__name__,
        obj_module=instance.__class__.__module__,
        obj_pk=instance.pk
    )