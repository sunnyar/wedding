from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import PageDetailView, GalleryDetailView, AudioFileDeleteView
from .views import PageListView, GalleryListView, AddressListView, AudioFileListView
from .views import PageUpdateView, AddressUpdateView, PhotoUpdateView, AudioFileUpdateView
from .views import PhotoCreateView, AudioFileCreateView
from .views import PhotoDeleteView, HomePageFormView, RsvpFormView
from .views import ContactFormView, ThemeFormView, PaymentFormView
from .views import rsvp_thanks, user_profile, homepage, about_us, contact_thanks
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('',
        url(r'^$', homepage, name='homepage'),
        url(r'^contact/$', ContactFormView.as_view(), name='contact_form'),
        url(r'^contact/thanks/$', contact_thanks, name='contact_thanks'),
        url(r'^terms/$', TemplateView.as_view(template_name='terms.html')),
        url(r'^big_video/$', TemplateView.as_view(template_name='example-ambient.html')),
        url(r'^themes/$', TemplateView.as_view(template_name='themes/select_theme.html'), {'theme_range' : range(65)}),
        #url(r'^premium_themes/$', TemplateView.as_view(template_name='themes/select_premium_theme.html'), {'theme_range' : range(33)}),
        url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html')),
        url(r'^about/$', about_us, name='about'),
        url(r'^payment/$', PaymentFormView.as_view(), name='payment_form'),
        url(r'^profile/$', user_profile),
        url(r'^(?P<username>[-\w\d]+)/theme$', ThemeFormView.as_view(), name='theme_form'),
        #url(r'^(?P<username>[-\w\d]+)/premium_theme$', PremiumThemeFormView.as_view(), name='premium_theme_form'),
        url(r'^audio/create/(?P<username>[-\w\d]+)$', auth(AudioFileCreateView.as_view()), name='audio_create'),
        url(r'^(?P<username>[-\w\d]+)/music-album$', AudioFileListView.as_view(), name='audio_list'),
        url(r'^audio/edit/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(AudioFileUpdateView.as_view()), name='audio_update'),
        url(r'^audio/delete/(?P<username>[-\w\d]+)/(?P<pk>[\d]+)$', auth(AudioFileDeleteView.as_view()), name='audio_delete'),
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
