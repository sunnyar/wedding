from django.conf.urls import patterns, url
from .views import PageDetailView, GalleryDetailView
from .views import PageListView, GalleryListView, AddressListView
from .views import PageUpdateView, AddressUpdateView, PhotoUpdateView
from .views import PhotoCreateView
from .views import PhotoDeleteView, HomePageFormView, RsvpFormView, ContactFormView, ThemeFormView
from .views import rsvp_thanks, user_profile, homepage, about_us, contact_thanks
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
        url(r'^$', homepage, name='homepage'),
        url(r'^contact/$', ContactFormView.as_view(), name='contact_form'),
        url(r'^contact/thanks/$', contact_thanks, name='contact_thanks'),
        url(r'^about/$', about_us, name='about'),
        url(r'^profile/$', user_profile),
        url(r'^(?P<username>[-\w\d]+)/theme$', ThemeFormView.as_view(), name='theme_form'),
        url(r'^profile/(?P<username>[-\w\d]+)$', HomePageFormView.as_view(), name='profile_form'),
        #url(r'^(?P<username>[-\w\d]+)/info$', GalleryListView.as_view(), name='gallery'),
        url(r'^(?P<username>[-\w\d]+)/(?P<pk>[\d]+)/photo$', GalleryDetailView.as_view(), name='photo_detail'),
        url(r'^(?P<username>[-\w\d]+)/photo-album$', GalleryListView.as_view(), name='photo_list'),
        url(r'^(?P<username>[-\w\d]+)/map-of-events$', AddressListView.as_view(), name='events_list'),
        url(r'^address/edit/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(AddressUpdateView.as_view()), name='address_update'),
        url(r'^(?P<username>[-\w\d]+)/rsvp$', RsvpFormView.as_view(), name='rsvp_form'),
        url(r'^(?P<username>[-\w\d]+)/rsvp/thanks$', rsvp_thanks, name='rsvp_thanks'),
        url(r'^(?P<username>[-\w\d]+)/homepage$', PageListView.as_view(), name='page_list'),
        url(r'^(?P<username>[-\w\d]+)/(?P<slug>[-\w\d]+)$', PageDetailView.as_view(), name='page_detail'),
        url(r'^edit/(?P<username>[-\w\d]+)/(?P<slug>[-\w\d]+)$', auth(PageUpdateView.as_view()), name='page_update'),
        url(r'^photo-album/create/(?P<username>[-\w\d]+)$', auth(PhotoCreateView.as_view()), name='photo_create'),
        url(r'^photo/edit/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(PhotoUpdateView.as_view()), name='photo_update'),
        url(r'^photo/delete/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(PhotoDeleteView.as_view()), name='photo_delete'),
)
