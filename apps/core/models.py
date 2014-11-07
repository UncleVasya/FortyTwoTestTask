from django.db import models


class OperationLog(models.Model):
    time = models.DateTimeField()
    operation = models.CharField(max_length=300)
    obj_class = models.CharField(max_length=300)
    obj_module = models.CharField(max_length=300)
    obj_pk = models.CharField(max_length=300)

    def __unicode__(self):
        return "%s  %s/%s/%s  %s" % \
               (self.operation, self.obj_module, self.obj_class,
                self.obj_pk, str(self.dtime))
