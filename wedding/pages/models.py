from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from photologue.models import Photo

class Page(models.Model):
    user  = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    slug  = models.SlugField()
    body  = models.TextField()
    created = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs) :
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self) :
        return reverse("page_detail", kwargs={"slug": str(self.slug)})


class Address(models.Model) :
    street = models.TextField()
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s, %s-%s, %s' % (self.street, self.city, self.zip_code, self.state)

    def get_absolute_url(self) :
        return reverse("events_list")

class Rsvp(models.Model) :
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

class PhotoAlbum(Photo) :

    def get_absolute_url(self) :
        super(PhotoAlbum, self).get_absolute_url()
        return reverse("gallery")