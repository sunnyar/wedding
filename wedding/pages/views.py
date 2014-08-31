from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import json
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, UpdateView
from .models import Page
from .forms import PageForm
from photologue.models import Photo
from .forms import PhotoForm
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from photologue.views import PhotoListView
from django.utils.text import slugify

class PageListView(ListView) :
    model = Page
    queryset = Page.objects.all()

class PageDetailView(DetailView) :
    model = Page

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['all_objects'] = Page.objects.all()
        return context

class PageUpdateView(UpdateView) :
    model = Page
    form_class = PageForm

class PhotoUpdateView(UpdateView) :
    model = Photo
    form_class = PhotoForm

class PhotoCreateView(CreateView):
    model = Photo
    form_class = PhotoForm

    def form_valid(self, form):
        isvalid = super(PhotoCreateView, self).form_valid(form)
        if self.request.FILES.get('image') :
            f = form.save(commit=False)
            f.slug = slugify(f.title)
            #m = Photo.objects.get_or_create(image=image)[0]
            f.save()
        return isvalid

    def get_success_url(self):
        return reverse('gallery')

class GalleryListView(PhotoListView) :
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['object_list_len'] = len(Photo.objects.all())
        context['page_list']       = Page.objects.all()
        return context


def show_map(request) :

    page_list = Page.objects.all()
    events    = ['Reception', 'Ceremony', 'Hotel']
    addresses = ['111A/102, Ashok Nagar, Kanpur', 'Kanha Continental, Kanpur', 'Hotel Landmark, Kanpur']
    map_events_list = zip(events, addresses)
    return render_to_response('pages/show_map.html', locals(), context_instance=RequestContext(request))
