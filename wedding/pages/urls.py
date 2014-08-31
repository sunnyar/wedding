from django.conf.urls import patterns, url
from .views import PageDetailView
from .views import PageListView
from .views import PageUpdateView
from .views import PhotoUpdateView
from .views import GalleryListView
from .views import PhotoCreateView
from .views import show_map

urlpatterns = patterns('',
        url(r'^photo-album$', GalleryListView.as_view(), name='gallery'),
        url(r'^map-of-events$', show_map, name='show_map'),
        url(r'^$', PageListView.as_view(), name='home'),
        url(r'^(?P<slug>[-\w\d]+)$', PageDetailView.as_view(), name='page_detail'),
        url(r'^edit/(?P<slug>[-\w\d]+)$', PageUpdateView.as_view(), name='page_update'),
        url(r'^photo-album/create/$', PhotoCreateView.as_view(), name='photo_create'),
        url(r'^photo/edit/(?P<slug>[-\w\d]+)$', PhotoUpdateView.as_view(), name='photo_update'),
)
