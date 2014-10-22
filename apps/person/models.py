from django.db import models


class Person(models.Model):
    # core data
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    # contacts data
    email = models.EmailField(null=True, blank=True)
    jabber = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=200, null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)
