from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from photologue.models import Photo
from datetime import datetime
from django.conf import settings
from audiofield.fields import AudioField
import os.path

class UserProfile(models.Model) :
    user        = models.OneToOneField(User, related_name='profile')
    user_domain = models.CharField(max_length=20, default='jack-and-jill')

    def __unicode__(self) :
        return '%s has %s domain' % (self.user, self.user_domain)

def content_file_name(instance, filename):
    return '/'.join(['images', instance.user.username, filename])

class Page(models.Model):
    user  = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    slug  = models.SlugField()
    image = models.ImageField("Heading Image", upload_to=content_file_name, null=True, blank=True)
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
    last_name  = models.CharField(max_length=15)
#    contact    = models.CharField(max_length=15)
    email      = models.EmailField()
#    connect    = models.CharField(verbose_name="How would you like us to contact you ?", max_length=15, choices=(('phone', 'Phone'), ('mail', 'E-Mail')), default=('phone', 'Phone'))
    response   = models.CharField(verbose_name="Will you and your family be attending ?", max_length=15, choices=(('yes', 'Yes'), ('no', 'No')), default=('tentative', 'Tentative'))

    def __unicode__(self):
        return '%s %s responsed %s to attend your wedding' % (self.first_name, self.last_name, self.response)


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


class Contact(models.Model) :
    full_name = models.CharField(verbose_name="Full Name", max_length=50)
    phone_num = models.CharField(verbose_name="Phone Number", max_length=20)
    email     = models.EmailField(verbose_name="Email Address")
    message   = models.TextField(verbose_name="Message")
    created   = models.DateTimeField()

    def __unicode__(self):
        return '%s (%s)' % (self.full_name, self.email)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.today()
        return super(Contact, self).save(*args, **kwargs)


class Theme(models.Model) :
    user  = models.ForeignKey(User)
    name  = models.CharField(verbose_name="Theme Name", max_length=10,
            choices=(('default', 'Default'), ('theme1', 'Theme1'), ('theme2', 'Theme2'), ('theme3', 'Theme3'),
                ('theme4', 'Theme4'), ('theme5', 'Theme5'), ('theme6', 'Theme6'),
                ('theme7', 'Theme7'), ('theme8', 'Theme8'), ('theme9', 'Theme9'),
                ('theme10', 'Theme10'), ('theme11', 'Theme11'), ('theme12', 'Theme12'),
                ('theme13', 'Theme13'), ('theme14', 'Theme14'), ('theme15', 'Theme15'),
                ('theme16', 'Theme16'), ('theme17', 'Theme17'), ('theme18', 'Theme18'),
                ('theme19', 'Theme19'), ('theme20', 'Theme20'), ('theme21', 'Theme21'),
                ('theme22', 'Theme22'), ('theme23', 'Theme23'), ('theme24', 'Theme24'),
                ('theme25', 'Theme25'), ('theme26', 'Theme26'), ('theme27', 'Theme27'),
                ('theme28', 'Theme28'), ('theme29', 'Theme29'), ('theme30', 'Theme30'),)
            , default=('default', 'Default'))