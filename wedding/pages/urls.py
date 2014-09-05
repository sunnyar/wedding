from django.conf.urls import patterns, url
from .views import PageDetailView
from .views import PageListView, GalleryListView, AddressListView
from .views import PageUpdateView, AddressUpdateView, PhotoUpdateView
from .views import PhotoCreateView
from .views import PhotoDeleteView, HomePageFormView
from .views import rsvp_reply, user_profile, homepage
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
        url(r'^$', homepage, name='homepage'),
        url(r'^profile/$', user_profile),
        url(r'^profile/(?P<username>[-\w\d]+)$', HomePageFormView.as_view(), name='profile_form'),
        url(r'^(?P<username>[-\w\d]+)/info$', GalleryListView.as_view(), name='gallery'),
        url(r'^(?P<username>[-\w\d]+)/photo-album$', GalleryListView.as_view(), name='gallery'),
        url(r'^(?P<username>[-\w\d]+)/map-of-events$', AddressListView.as_view(), name='events_list'),
        url(r'^address/edit/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(AddressUpdateView.as_view()), name='address_update'),
        url(r'^(?P<username>[-\w\d]+)/homepage$', PageListView.as_view(), name='page_list'),
        url(r'^(?P<username>[-\w\d]+)/(?P<slug>[-\w\d]+)$', PageDetailView.as_view(), name='page_detail'),
        url(r'^edit/(?P<username>[-\w\d]+)/(?P<slug>[-\w\d]+)$', auth(PageUpdateView.as_view()), name='page_update'),
        url(r'^photo-album/create/(?P<username>[-\w\d]+)$', auth(PhotoCreateView.as_view()), name='photo_create'),
        url(r'^photo/edit/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(PhotoUpdateView.as_view()), name='photo_update'),
        url(r'^photo/delete/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(PhotoDeleteView.as_view()), name='photo_delete'),
        url(r'^rsvp/thanks$', rsvp_reply, name='rsvp_reply'),
)
