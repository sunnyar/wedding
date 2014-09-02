from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import json
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, UpdateView
from .models import Page, PhotoContent
from .models import Address
from .forms import PageForm
from .forms import AddressForm, RsvpForm, PhotoForm
from photologue.models import Photo
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from photologue.views import PhotoListView
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from collections import OrderedDict

wedding_pages = OrderedDict([('Welcome' , 'Welcome to our Wedding'), ('About Us', ''),
    ('Our Proposal', ''), ('Ceremony', ''), ('Reception', ''), ('Wedding Party',  ''),
        ('Guest Information', ''), ('Photo Album', ''), ('Map of Events',  ''),
            ('RSVP', '')])


def homepage(request) :
    return render_to_response('index.html', {'wedding_pages' : wedding_pages }, context_instance=RequestContext(request))


class PageListView(ListView) :
    model = Page

    def get_queryset(self) :
        queryset = Page.objects.filter(user=self.request.user)
        for page, body in wedding_pages.items() :
            if not Page.objects.filter(user=self.request.user, title=page).exists() :
                Page.objects.create(user=self.request.user, title=page, body=body, created=datetime.now())
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        return context

class PageDetailView(DetailView) :
    model = Page

    def get_queryset(self) :
        queryset = Page.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        context['logged_user'] = self.request.user
        return context

class PageUpdateView(UpdateView) :
    model = Page
    form_class = PageForm

    def get_queryset(self) :
        queryset = Page.objects.filter(user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("page_detail", kwargs={"username" : str(self.request.user), "slug": str(self.object.slug)})

    def get_context_data(self, **kwargs):
        context = super(PageUpdateView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

class PhotoUpdateView(UpdateView) :
    model = PhotoContent
    form_class = PhotoForm
    template_name = 'photologue/photo_form.html'

    def get_queryset(self) :
        queryset = PhotoContent.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhotoUpdateView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('gallery', kwargs={"username" : str(self.request.user)} )


class PhotoCreateView(CreateView):
    model = PhotoContent
    form_class = PhotoForm
    template_name = 'photologue/photo_form.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoCreateView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        if self.request.FILES.get('image') :
            f = form.save(commit=False)
            f.user = self.request.user
            f.slug = slugify(f.title)
            #m = Photo.objects.get_or_create(image=image)[0]
            f.save()
        isvalid = super(PhotoCreateView, self).form_valid(form)
        return isvalid

    def get_success_url(self):
        return reverse('gallery', kwargs={"username" : str(self.request.user)} )

class PhotoDeleteView(DeleteView) :
    model = PhotoContent
    #success_url = reverse_lazy('gallery', kwargs={"username" : str(request.user)})
    template_name = 'photologue/photo_confirm_delete.html'

    def get_queryset(self) :
        queryset = PhotoContent.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhotoDeleteView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self) :
        return reverse('gallery', kwargs={"username" : str(self.request.user)})


class GalleryListView(PhotoListView) :
    model = PhotoContent
    template_name = 'photologue/photo_list.html'
    paginate_by = 20

    def get_queryset(self) :
        queryset = PhotoContent.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['object_list_len'] = len(PhotoContent.objects.filter(user=self.request.user))
        context['page_list']       = Page.objects.filter(user=self.request.user)
        context['logged_user']     = self.request.user
        return context


class AddressListView(ListView) :

    model = Address
    queryset = Address.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AddressListView, self).get_context_data(**kwargs)
        context['page_list'] = Page.objects.all()
        events    = ['Reception', 'Ceremony', 'Hotel']
        addresses = Address.objects.all()
        context['map_events_list'] = zip(events, addresses)
        return context

class AddressUpdateView(UpdateView) :
    model = Address
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['all_objects'] = Page.objects.all()
        return context

def rsvp_reply(request) :
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid() :
            form.save(commit=False)
            all_objects = Page.objects.all()
            form.save()
            return render_to_response('pages/thanks.html',locals(), context_instance=RequestContext(request))
    else :
        pass