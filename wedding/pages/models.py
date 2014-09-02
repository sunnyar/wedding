from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from photologue.models import Photo
from datetime import datetime

class Page(models.Model):
    user  = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    slug  = models.SlugField()
    image = models.ImageField("Heading Image", upload_to="images/", null=True, blank=True)
    body  = models.TextField()
    created = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs) :
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)


class Address(models.Model) :
    user  = models.ForeignKey(User)
    event = models.CharField(max_length=20)
    street = models.TextField()
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s:%s, %s-%s, %s' % (self.event, self.street, self.city, self.zip_code, self.state)


class Rsvp(models.Model) :
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class PhotoContent(Photo) :
    user  = models.ForeignKey(User)