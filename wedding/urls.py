from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wedding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', homepage, name='homepage'),
    url(r'^',include('wedding.pages.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^photologue/', include('photologue.urls')),
    (r'^accounts/', include('allauth.urls')),
    (r'^summernote/', include('django_summernote.urls')),
)
