from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save)
def object_saved(sender, instance, created, raw, using, **kwargs):
    pass


@receiver(post_delete)
def object_deleted(sender, instance, using, **kwargs):
    pass
