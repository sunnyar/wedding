from django.conf.urls import patterns, include, url
from pages.views import homepage

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wedding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', homepage, name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^photologue/', include('photologue.urls')),
    (r'^accounts/', include('allauth.urls')),
    url(r'^homepage/', include('wedding.pages.urls')),
)
