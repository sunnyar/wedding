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


from django.core.exceptions import ValidationError
from datetime import date

def wedding_date_validator(value) :
    if value <= date.today() :
        raise ValidationError('Provide a Wedding Date after %s' % (date.today().strftime('%m-%d-%Y')))

class Wedding(models.Model) :
    user  = models.ForeignKey(User)
    groom_first_name = models.CharField(verbose_name="Groom's First Name", max_length=20)
    groom_last_name = models.CharField(verbose_name="Groom's Last Name", max_length=20)
    bride_first_name = models.CharField(verbose_name="Bride's First Name", max_length=20)
    bride_last_name = models.CharField(verbose_name="Bride's Last Name", max_length=20)
    location = models.CharField(verbose_name="Wedding Location", max_length=20)
    wedding_date = models.DateField(verbose_name='Wedding Date', validators=[wedding_date_validator])

    def __unicode__(self):
        return '%s %s & %s %s Wedding\n%s' % (self.groom_first_name, self.groom_last_name, self.bride_first_name, self.bride_last_name, self.wedding_date)