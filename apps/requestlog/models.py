from django.db import models


class RequestLog(models.Model):
    # data
    path = models.CharField(max_length=300)
    method = models.CharField(max_length=4)
    query = models.CharField(max_length=500, null=True, blank=True)
    address = models.IPAddressField(null=True, blank=True)
    # time and result
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    response_code = models.IntegerField()
    # additional
    priority = models.PositiveIntegerField(
        default=1,
        choices=[(i, i) for i in range(1, 11)]
    )

    def __unicode__(self):
        return "%s  %s  %s" % (self.path, self.address, str(self.time_start))
