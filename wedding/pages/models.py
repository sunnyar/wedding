from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from photologue.models import Photo
from datetime import datetime
from django.conf import settings
from audiofield.fields import AudioField
import os.path
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

class UserProfile(models.Model) :
    user        = models.OneToOneField(User, related_name='profile')
    user_domain = models.CharField(max_length=20, default='jack-and-jill')
    member      = models.BooleanField(default=False)
    access_key  = models.CharField(max_length=10, default='0000000')
    access_granted = models.BooleanField(default=False)

    def __unicode__(self) :
        if self.member :
            return '%s has %s domain and is a Premium Member with access key : %s' % (self.user, self.user_domain, self.access_key)
        else :
            return '%s has %s domain and is a Free Member with access key : %s' % (self.user, self.user_domain, self.access_key)


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


THEMES_CHOICES = (
    ('default', mark_safe(_('<img src="%(media_url)simages/themes/theme0.jpg" \
        width="250" height="250" alt="default" title="Default Theme">' \
        % {'media_url': settings.MEDIA_URL, },))),
    ("theme1", mark_safe(_('<img src="%(media_url)simages/themes/theme1.jpg" \
        width="250" height="250" alt="theme1" title="Theme1">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme2", mark_safe(_('<img src="%(media_url)simages/themes/theme2.jpg" \
        width="250" height="250" alt="theme2" title="Theme2">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme3", mark_safe(_('<img src="%(media_url)simages/themes/theme3.jpg" \
        width="250" height="250" alt="theme3" title="Theme3">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme4", mark_safe(_('<img src="%(media_url)simages/themes/theme4.jpg" \
        width="250" height="250" alt="theme4" title="Theme4">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme5", mark_safe(_('<img src="%(media_url)simages/themes/theme5.jpg" \
        width="250" height="250" alt="theme5" title="Theme5">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme6", mark_safe(_('<img src="%(media_url)simages/themes/theme6.jpg" \
        width="250" height="250" alt="theme6" title="Theme6">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme7", mark_safe(_('<img src="%(media_url)simages/themes/theme7.jpg" \
        width="250" height="250" alt="theme7" title="Theme7">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme8", mark_safe(_('<img src="%(media_url)simages/themes/theme8.jpg" \
        width="250" height="250" alt="theme8" title="Theme8">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme9", mark_safe(_('<img src="%(media_url)simages/themes/theme9.jpg" \
        width="250" height="250" alt="theme9" title="Theme9">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme10", mark_safe(_('<img src="%(media_url)simages/themes/theme10.jpg" \
        width="250" height="250" alt="theme10" title="Theme10">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme11", mark_safe(_('<img src="%(media_url)simages/themes/theme11.jpg" \
        width="250" height="250" alt="theme11" title="Theme11">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme12", mark_safe(_('<img src="%(media_url)simages/themes/theme12.jpg" \
        width="250" height="250" alt="theme12" title="Theme12">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme13", mark_safe(_('<img src="%(media_url)simages/themes/theme13.jpg" \
        width="250" height="250" alt="theme13" title="Theme13">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme14", mark_safe(_('<img src="%(media_url)simages/themes/theme14.jpg" \
        width="250" height="250" alt="theme14" title="Theme14">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme15", mark_safe(_('<img src="%(media_url)simages/themes/theme15.jpg" \
        width="250" height="250" alt="theme15" title="Theme15">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme16", mark_safe(_('<img src="%(media_url)simages/themes/theme16.jpg" \
        width="250" height="250" alt="theme16" title="Theme16">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme17", mark_safe(_('<img src="%(media_url)simages/themes/theme17.jpg" \
        width="250" height="250" alt="theme17" title="Theme17">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme18", mark_safe(_('<img src="%(media_url)simages/themes/theme18.jpg" \
        width="250" height="250" alt="theme18" title="Theme18">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme19", mark_safe(_('<img src="%(media_url)simages/themes/theme19.jpg" \
        width="250" height="250" alt="theme19" title="Theme19">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme20", mark_safe(_('<img src="%(media_url)simages/themes/theme20.jpg" \
        width="250" height="250" alt="theme20" title="Theme20">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme21", mark_safe(_('<img src="%(media_url)simages/themes/theme21.jpg" \
        width="250" height="250" alt="theme21" title="Theme21">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme22", mark_safe(_('<img src="%(media_url)simages/themes/theme22.jpg" \
        width="250" height="250" alt="theme22" title="Theme22">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme23", mark_safe(_('<img src="%(media_url)simages/themes/theme23.jpg" \
        width="250" height="250" alt="theme23" title="Theme23">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme24", mark_safe(_('<img src="%(media_url)simages/themes/theme24.jpg" \
        width="250" height="250" alt="theme24" title="Theme24">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme25", mark_safe(_('<img src="%(media_url)simages/themes/theme25.jpg" \
        width="250" height="250" alt="theme25" title="Theme25">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme26", mark_safe(_('<img src="%(media_url)simages/themes/theme26.jpg" \
        width="250" height="250" alt="theme26" title="Theme26">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme27", mark_safe(_('<img src="%(media_url)simages/themes/theme27.jpg" \
        width="250" height="250" alt="theme27" title="Theme27">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme28", mark_safe(_('<img src="%(media_url)simages/themes/theme28.jpg" \
        width="250" height="250" alt="theme28" title="Theme28">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme29", mark_safe(_('<img src="%(media_url)simages/themes/theme29.jpg" \
        width="250" height="250" alt="theme29" title="Theme29">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("theme30", mark_safe(_('<img src="%(media_url)simages/themes/theme30.jpg" \
        width="250" height="250" alt="theme30" title="Theme30">' \
        % {"media_url": settings.MEDIA_URL, },))),


    ('premium_theme0', mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme0.jpg" \
        width="250" height="250" alt="premium_theme0" title="Premium_Theme0">' \
        % {'media_url': settings.MEDIA_URL, },))),
    ("premium_theme1", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme1.jpg" \
        width="250" height="250" alt="premium_theme1" title="Premium_Theme1">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme2", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme2.jpg" \
        width="250" height="250" alt="premium_theme2" title="Premium_Theme2">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme3", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme3.jpg" \
        width="250" height="250" alt="premium_theme3" title="Premium_Theme3">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme4", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme4.jpg" \
        width="250" height="250" alt="premium_theme4" title="Premium_Theme4">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme5", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme5.jpg" \
        width="250" height="250" alt="premium_theme5" title="Premium_Theme5">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme6", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme6.jpg" \
        width="250" height="250" alt="premium_theme6" title="Premium_Theme6">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme7", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme7.jpg" \
        width="250" height="250" alt="premium_theme7" title="Premium_Theme7">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme8", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme8.jpg" \
        width="250" height="250" alt="premium_theme8" title="Premium_Theme8">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme9", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme9.jpg" \
        width="250" height="250" alt="premium_theme9" title="Premium_Theme9">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme10", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme10.jpg" \
        width="250" height="250" alt="premium_theme10" title="Premium_Theme10">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme11", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme11.jpg" \
        width="250" height="250" alt="premium_theme11" title="Premium_Theme11">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme12", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme12.jpg" \
        width="250" height="250" alt="premium_theme12" title="Premium_Theme12">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme13", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme13.jpg" \
        width="250" height="250" alt="premium_theme13" title="Premium_Theme13">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme14", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme14.jpg" \
        width="250" height="250" alt="premium_theme14" title="Premium_Theme14">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme15", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme15.jpg" \
        width="250" height="250" alt="premium_theme15" title="Premium_Theme15">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme16", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme16.jpg" \
        width="250" height="250" alt="premium_theme16" title="Premium_Theme16">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme17", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme17.jpg" \
        width="250" height="250" alt="premium_theme17" title="Premium_Theme17">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme18", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme18.jpg" \
        width="250" height="250" alt="premium_theme18" title="Premium_Theme18">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme19", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme19.jpg" \
        width="250" height="250" alt="premium_theme19" title="Premium_Theme19">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme20", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme20.jpg" \
        width="250" height="250" alt="premium_theme20" title="Premium_Theme20">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme21", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme21.jpg" \
        width="250" height="250" alt="premium_theme21" title="Premium_Theme21">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme22", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme22.jpg" \
        width="250" height="250" alt="premium_theme22" title="Premium_Theme22">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme23", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme23.jpg" \
        width="250" height="250" alt="premium_theme23" title="Premium_Theme23">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme24", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme24.jpg" \
        width="250" height="250" alt="premium_theme24" title="Premium_Theme24">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme25", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme25.jpg" \
        width="250" height="250" alt="premium_theme25" title="Premium_Theme25">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme26", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme26.jpg" \
        width="250" height="250" alt="premium_theme26" title="Premium_Theme26">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme27", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme27.jpg" \
        width="250" height="250" alt="premium_theme27" title="Premium_Theme27">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme28", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme28.jpg" \
        width="250" height="250" alt="premium_theme28" title="Premium_Theme28">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme29", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme29.jpg" \
        width="250" height="250" alt="premium_theme29" title="Premium_Theme29">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme30", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme30.jpg" \
        width="250" height="250" alt="premium_theme30" title="Premium_Theme30">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme31", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme31.jpg" \
        width="250" height="250" alt="premium_theme31" title="Premium_Theme31">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme32", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme32.jpg" \
        width="250" height="250" alt="premium_theme32" title="Premium_Theme32">' \
        % {"media_url": settings.MEDIA_URL, },))),
)


PREMIUM_THEMES_CHOICES = (
    ('premium_theme0', mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme0.jpg" \
        width="250" height="250" alt="premium_theme0" title="Premium_Theme0">' \
        % {'media_url': settings.MEDIA_URL, },))),
    ("premium_theme1", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme1.jpg" \
        width="250" height="250" alt="premium_theme1" title="Premium_Theme1">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme2", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme2.jpg" \
        width="250" height="250" alt="premium_theme2" title="Premium_Theme2">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme3", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme3.jpg" \
        width="250" height="250" alt="premium_theme3" title="Premium_Theme3">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme4", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme4.jpg" \
        width="250" height="250" alt="premium_theme4" title="Premium_Theme4">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme5", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme5.jpg" \
        width="250" height="250" alt="premium_theme5" title="Premium_Theme5">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme6", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme6.jpg" \
        width="250" height="250" alt="premium_theme6" title="Premium_Theme6">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme7", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme7.jpg" \
        width="250" height="250" alt="premium_theme7" title="Premium_Theme7">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme8", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme8.jpg" \
        width="250" height="250" alt="premium_theme8" title="Premium_Theme8">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme9", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme9.jpg" \
        width="250" height="250" alt="premium_theme9" title="Premium_Theme9">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme10", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme10.jpg" \
        width="250" height="250" alt="premium_theme10" title="Premium_Theme10">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme11", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme11.jpg" \
        width="250" height="250" alt="premium_theme11" title="Premium_Theme11">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme12", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme12.jpg" \
        width="250" height="250" alt="premium_theme12" title="Premium_Theme12">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme13", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme13.jpg" \
        width="250" height="250" alt="premium_theme13" title="Premium_Theme13">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme14", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme14.jpg" \
        width="250" height="250" alt="premium_theme14" title="Premium_Theme14">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme15", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme15.jpg" \
        width="250" height="250" alt="premium_theme15" title="Premium_Theme15">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme16", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme16.jpg" \
        width="250" height="250" alt="premium_theme16" title="Premium_Theme16">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme17", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme17.jpg" \
        width="250" height="250" alt="premium_theme17" title="Premium_Theme17">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme18", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme18.jpg" \
        width="250" height="250" alt="premium_theme18" title="Premium_Theme18">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme19", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme19.jpg" \
        width="250" height="250" alt="premium_theme19" title="Premium_Theme19">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme20", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme20.jpg" \
        width="250" height="250" alt="premium_theme20" title="Premium_Theme20">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme21", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme21.jpg" \
        width="250" height="250" alt="premium_theme21" title="Premium_Theme21">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme22", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme22.jpg" \
        width="250" height="250" alt="premium_theme22" title="Premium_Theme22">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme23", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme23.jpg" \
        width="250" height="250" alt="premium_theme23" title="Premium_Theme23">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme24", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme24.jpg" \
        width="250" height="250" alt="premium_theme24" title="Premium_Theme24">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme25", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme25.jpg" \
        width="250" height="250" alt="premium_theme25" title="Premium_Theme25">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme26", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme26.jpg" \
        width="250" height="250" alt="premium_theme26" title="Premium_Theme26">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme27", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme27.jpg" \
        width="250" height="250" alt="premium_theme27" title="Premium_Theme27">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme28", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme28.jpg" \
        width="250" height="250" alt="premium_theme28" title="Premium_Theme28">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme29", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme29.jpg" \
        width="250" height="250" alt="premium_theme29" title="Premium_Theme29">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme30", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme30.jpg" \
        width="250" height="250" alt="premium_theme30" title="Premium_Theme30">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme31", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme31.jpg" \
        width="250" height="250" alt="premium_theme31" title="Premium_Theme31">' \
        % {"media_url": settings.MEDIA_URL, },))),
    ("premium_theme32", mark_safe(_('<img src="%(media_url)simages/premium_themes/premium_theme32.jpg" \
        width="250" height="250" alt="premium_theme32" title="Premium_Theme32">' \
        % {"media_url": settings.MEDIA_URL, },))),
)


class Theme(models.Model) :
    """(('default', 'Default'), ('theme1', 'Theme1'), ('theme2', 'Theme2'), ('theme3', 'Theme3'),
                ('theme4', 'Theme4'), ('theme5', 'Theme5'), ('theme6', 'Theme6'),
                ('theme7', 'Theme7'), ('theme8', 'Theme8'), ('theme9', 'Theme9'),
                ('theme10', 'Theme10'), ('theme11', 'Theme11'), ('theme12', 'Theme12'),
                ('theme13', 'Theme13'), ('theme14', 'Theme14'), ('theme15', 'Theme15'),
                ('theme16', 'Theme16'), ('theme17', 'Theme17'), ('theme18', 'Theme18'),
                ('theme19', 'Theme19'), ('theme20', 'Theme20'), ('theme21', 'Theme21'),
                ('theme22', 'Theme22'), ('theme23', 'Theme23'), ('theme24', 'Theme24'),
                ('theme25', 'Theme25'), ('theme26', 'Theme26'), ('theme27', 'Theme27'),
                ('theme28', 'Theme28'), ('theme29', 'Theme29'), ('theme30', 'Theme30'),)
                """
    user  = models.ForeignKey(User)
    name  = models.CharField(verbose_name="Theme Name", max_length=100,
                choices= THEMES_CHOICES, default=('default', 'Default'))
"""
class PremiumTheme(models.Model) :

    user   = models.ForeignKey(User)
    member = models.BooleanField(default=True)
    name   = models.CharField(verbose_name="Theme Name", max_length=100,
                choices= PREMIUM_THEMES_CHOICES, default=('premium_theme0', 'Premium_Theme0'))
"""