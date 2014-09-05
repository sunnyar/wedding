from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView, UpdateView
from .models import Page, PhotoContent, Wedding
from .models import Address
from .forms import PageForm
from .forms import AddressForm, RsvpForm, PhotoForm, WeddingForm
from photologue.models import Photo
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView, FormView
from photologue.views import PhotoListView, PhotoDetailView
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from collections import OrderedDict

wedding_pages = OrderedDict([('HomePage', '<center><h1>My Home Page.</h1></center><br><p><font size="3">Start creating your website and edit the pages as per your need and information.<br> Share with your near and dear ones</font></p><br><p><b>Demo :</b></p>'),
    ('Welcome' , '<center><b>Welcome to our wedding website !!</b><center><br><p>We can\'t wait to get married. We\'re so excited to share our special day with our friends and family!</p>'),
    ('About Us', '<h2>About the Groom</h2><br><p>Tell your guests about your partner.</p><br><h2>About the Bride</h2><br><p>Tell your guests about your partner.</p><br><h2>How We Met</h2><br><p>Tell your guests a little about how you met.</p>'),
    ('Our Proposal', '<h2>When It Happened</h2><br><p>Date you met / Got Engaged</p><br><br><h2>How We Got Engaged</h2><br><p>Some memories of your Love Story, a little about how you met.</p>'),
    ('Ceremony', '<h2>Information For Our Guests</h2><br><p>Provide information about the event.</p><br><h2>Driving Directions</h2><br><p>Give guests directions to the event.</p><br><h2>Additional Information</h2><br><p>Tell your guests any additional information you want them to know.</p>'),
    ('Reception', '<h2>Information For Our Guests</h2><br><p>Provide information about the event.</p><br><h2>Driving Directions</h2><br><p>Give guests directions to the event.</p><br><h2>Additional Information</h2><br><p><Tell your guests any additional information you want them to know.</p>'),
    ('Wedding Party', '<h2>Our Wedding Party</h2><br><p>Details about the party and family</p>'),
    ('Guest Information', '<h2>Hotel Accommodations</h2><br><p>Hotel details/Contact no/Address</p><br><br><h2>Things To Do in the Area</h2><br><br><p>Tell your guests what they can do in the area.</p><br><h2>Additional information</h2><br><p>Tell your guests any additional information you want them to know.</p>'),
    ('Photo Album', ''), ('Map of Events',  ''),
    ('RSVP', '<h2>RSVP Information</h2><br><br><p>To RSVP online to Jack and Jill\'s wedding, enter your name in the box below.<br>Only enter one name in your party as it appeared on your invitation using the following format: Jack Smith</p><br><br><p>Do not enter prefixes such as Mr., Mrs., Dr., etc.</p><br><br>')])

address_dict = OrderedDict([('Ceremony' ,['Kanha Continental', 'Kanpur', 'UP', '208012']),
                            ('Reception', ['111A/102, Ashok Nagar', 'Kanpur', 'UP', '208012']),
                            ('Hotel', ['Landmark Towers', 'Kanpur', 'UP', '208012'])])


def homepage(request) :
    return render_to_response('index.html', {'wedding_pages' : wedding_pages}, context_instance=RequestContext(request))

@login_required
def user_profile(request):
    return HttpResponseRedirect(reverse('profile_form', kwargs={"username" : request.user.username}))

class HomePageFormView(FormView):

    template_name = 'pages/wedding.html'
    form_class = WeddingForm

    def get_success_url(self):
        return reverse("page_list", kwargs={"username" : self.request.user})

    def get_context_data(self, **kwargs):
        context = super(HomePageFormView, self).get_context_data(**kwargs)
        context['wedding_objects'] = Wedding.objects.filter(user=self.request.user)
        context['username'] = self.request.user
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if not Wedding.objects.filter(user=self.request.user).exists() :
            Wedding.objects.create(user=self.request.user,
                groom_first_name=form.cleaned_data['groom_first_name'],
                groom_last_name=form.cleaned_data['groom_last_name'],
                bride_first_name=form.cleaned_data['bride_first_name'],
                bride_last_name=form.cleaned_data['bride_last_name'],
                location=form.cleaned_data['location'],
                wedding_date=form.cleaned_data['wedding_date'])
        else :
            Wedding.objects.all().update(user=self.request.user,
                groom_first_name=form.cleaned_data['groom_first_name'],
                groom_last_name=form.cleaned_data['groom_last_name'],
                bride_first_name=form.cleaned_data['bride_first_name'],
                bride_last_name=form.cleaned_data['bride_last_name'],
                location=form.cleaned_data['location'],
                wedding_date=form.cleaned_data['wedding_date'])
        return super(HomePageFormView, self).form_valid(form)


class PageListView(ListView) :
    model = Page

    def get_queryset(self) :
        username=self.kwargs['username']
        queryset = Page.objects.filter(user__username=username)
        if self.request.user.is_authenticated :
            for page, body in wedding_pages.items() :
                if not Page.objects.filter(user=self.request.user, title=page).exists() :
                    Page.objects.create(user=self.request.user, title=page, body=body, created=datetime.now())
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        context['wedding_objects'] = Wedding.objects.filter(user__username=self.kwargs['username'])
        return context

class PageDetailView(DetailView) :
    model = Page

    def get_queryset(self) :
        username = self.kwargs['username']
        queryset = Page.objects.filter(user__username=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        logged_user = self.request.user
        username    = self.kwargs['username']

        context['all_objects'] = Page.objects.filter(user__username=username)
        context['username']    = self.kwargs['username']
        context['wedding_objects'] = Wedding.objects.filter(user__username=username)

        if logged_user.is_authenticated :
            context['logged_user'] = logged_user

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
        return reverse('photo_list', kwargs={"username" : str(self.request.user)} )


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
        return reverse('photo_list', kwargs={"username" : str(self.request.user)} )

class PhotoDeleteView(DeleteView) :
    model = PhotoContent
    #success_url = reverse_lazy('photo_list', kwargs={"username" : str(request.user)})
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
        return reverse('photo_list', kwargs={"username" : str(self.request.user)})


class GalleryListView(PhotoListView) :
    model = PhotoContent
    template_name = 'photologue/photo_list.html'
    paginate_by = 20

    def get_queryset(self) :
        username = self.kwargs['username']
        queryset = PhotoContent.objects.filter(user__username=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        logged_user = self.request.user
        username    = self.kwargs['username']

        context['object_list_len'] = len(PhotoContent.objects.filter(user__username=username))
        context['page_list']       = Page.objects.filter(user__username=username)
        context['wedding_objects'] = Wedding.objects.filter(user__username=username)
        context['username']        = username

        if logged_user.is_authenticated :
            context['logged_user']     = self.request.user
        return context

class GalleryDetailView(PhotoDetailView) :
    model = PhotoContent
    template_name = 'photologue/photo_detail.html'

    def get_queryset(self) :
        username = self.kwargs['username']
        queryset = PhotoContent.objects.filter(user__username=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        logged_user = self.request.user
        username    = self.kwargs['username']

        context['object_list_len'] = len(PhotoContent.objects.filter(user__username=username))
        context['page_list']       = Page.objects.filter(user__username=username)
        context['wedding_objects'] = Wedding.objects.filter(user__username=username)
        context['username']        = username

        if logged_user.is_authenticated :
            context['logged_user']     = self.request.user
        return context


class AddressListView(ListView) :

    model = Address
    template_name = 'pages/address_list.html'

    def get_queryset(self) :
        username    = self.kwargs['username']
        queryset = Address.objects.filter(user__username=username)

        if self.request.user.is_authenticated :
            if not Address.objects.filter(user__username=username).exists() :
                for event, address in address_dict.items() :
                    Address.objects.create(user=self.request.user, event=event, street=address[0], city=address[1], state=address[2], zip_code=address[3])
        return queryset


    def get_context_data(self, **kwargs):
        context = super(AddressListView, self).get_context_data(**kwargs)
        username    = self.kwargs['username']
        logged_user = self.request.user

        context['page_list'] = Page.objects.filter(user__username=username)
        context['addresses'] = Address.objects.filter(user__username=username)
        context['wedding_objects'] = Wedding.objects.filter(user__username=username)
        context['username']  = username

        if logged_user.is_authenticated :
            context['logged_user'] = logged_user

        return context


class AddressUpdateView(UpdateView) :
    model = Address
    form_class = AddressForm
    template_name = 'pages/address_form.html'

    def get_queryset(self) :
        queryset = Address.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self) :
        return reverse('events_list', kwargs={"username" : str(self.request.user)})


def rsvp_reply(request) :
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid() :
            form.save(commit=False)
            all_objects = Page.objects.filter(request.user)
            form.save()
            return render_to_response('pages/thanks.html',locals(), context_instance=RequestContext(request))
    else :
        pass


class RsvpFormView(FormView):

    template_name = 'pages/rsvp_form.html'
    form_class = RsvpForm

    def get_success_url(self):
        return reverse("page_detail", kwargs={"username" : self.kwargs['username'], "slug" : self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(RsvpFormView, self).get_context_data(**kwargs)
        context['wedding_objects'] = Wedding.objects.filter(user=self.request.user)
        context['username'] = self.request.user
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if not Wedding.objects.filter(user=self.request.user).exists() :
            Wedding.objects.create(user=self.request.user,
                groom_first_name=form.cleaned_data['groom_first_name'],
                groom_last_name=form.cleaned_data['groom_last_name'],
                bride_first_name=form.cleaned_data['bride_first_name'],
                bride_last_name=form.cleaned_data['bride_last_name'],
                location=form.cleaned_data['location'],
                wedding_date=form.cleaned_data['wedding_date'])
        else :
            Wedding.objects.all().update(user=self.request.user,
                groom_first_name=form.cleaned_data['groom_first_name'],
                groom_last_name=form.cleaned_data['groom_last_name'],
                bride_first_name=form.cleaned_data['bride_first_name'],
                bride_last_name=form.cleaned_data['bride_last_name'],
                location=form.cleaned_data['location'],
                wedding_date=form.cleaned_data['wedding_date'])
        return super(HomePageFormView, self).form_valid(form)
