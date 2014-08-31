from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

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
