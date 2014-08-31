from django.conf.urls import patterns, url
from .views import PageDetailView
from .views import PageListView, GalleryListView, AddressListView
from .views import PageUpdateView, AddressUpdateView, PhotoUpdateView
from .views import PhotoCreateView
from .views import PhotoDeleteView
from .views import rsvp_reply
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
        url(r'^photo-album$', GalleryListView.as_view(), name='gallery'),
        url(r'^map-of-events$', AddressListView.as_view(), name='events_list'),
        url(r'^address/edit/(?P<pk>[\d]+)$', auth(AddressUpdateView.as_view()), name='address_update'),
        url(r'^$', PageListView.as_view(), name='home'),
        url(r'^(?P<slug>[-\w\d]+)$', PageDetailView.as_view(), name='page_detail'),
        url(r'^edit/(?P<slug>[-\w\d]+)$', auth(PageUpdateView.as_view()), name='page_update'),
        url(r'^photo-album/create/$', auth(PhotoCreateView.as_view()), name='photo_create'),
        url(r'^photo/edit/(?P<pk>[\d]+)$', auth(PhotoUpdateView.as_view()), name='photo_update'),
        url(r'^photo/delete/(?P<pk>[\d]+)$', auth(PhotoDeleteView.as_view()), name='photo_delete'),
        url(r'^rsvp/thanks$', rsvp_reply, name='rsvp_reply'),
)
