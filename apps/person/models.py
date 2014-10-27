from PIL import Image
from django.db import models


class Person(models.Model):
    # core data
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    # contacts data
    email = models.EmailField(null=True, blank=True)
    jabber = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=200, null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)

    def save(self):
        super(Person, self).save()

        # if self.photo:
        #     photo_size = {'height': 350, 'width': 500}
        #
        #     photo = Image.open(self.photo.path)
        #     photo.thumbnail((photo_size['width'], photo_size['height']),
        #                     Image.ANTIALIAS)
        #     photo.save(self.photo.path)
