from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, UpdateView
from .models import Page, PhotoContent, Wedding
from .models import Address, Rsvp, UserProfile, Theme
from .forms import PageForm, ThemeForm, AudioFileForm, PaymentForm, SiteAccessForm
from .forms import AddressForm, RsvpForm, PhotoForm, WeddingForm, ContactForm
from .cookiemixin import CookieMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, FormMixin
from django.views.generic.edit import DeleteView, FormView
from photologue.views import PhotoListView, PhotoDetailView
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from collections import OrderedDict
from django.core.mail import send_mail
from allauth.account.views import EmailAddress
from audiofield.models import AudioFile
import random, string
from django.contrib.sites.models import Site
from geopy import geocoders




wedding_pages = OrderedDict([('HomePage', ''), #<center><h1>My Home Page.</h1><br><p><font size="3">Start creating your website and edit the pages as per your need and information.<br> You can also check our demo site <a href="/sunnyarora07/welcome"><b>Here</b></a></font></p></center><br><p><b>Edit Instructions :</b></p><br>'),
    ('Welcome' , '<center><b>Welcome to our wedding website !!</b><p>We can\'t wait to get married. We\'re so excited to share our special day with our friends and family!</p></center>'),
    ('About Us', '<h2>About the Groom</h2><p>Tell your guests about your partner.</p><br><h2>About the Bride</h2><p>Tell your guests about your partner.</p><br><h2>How We Met</h2><p>Tell your guests a little about how you met.</p>'),
    ('Our Proposal', '<h2>When It Happened</h2><p>Date you met / Got Engaged</p><br><h2>How We Got Engaged</h2><p>Some memories of your Love Story, a little about how you met.</p>'),
    ('Ceremony', '<h2>Information For Our Guests</h2><p>Provide information about the event.</p><br><h2>Driving Directions</h2><p>Give guests directions to the event.</p><br><h2>Additional Information</h2><p>Tell your guests any additional information you want them to know.</p>'),
    ('Reception', '<h2>Information For Our Guests</h2><p>Provide information about the event.</p><br><h2>Driving Directions</h2><p>Give guests directions to the event.</p><br><h2>Additional Information</h2><p><Tell your guests any additional information you want them to know.</p>'),
    ('Wedding Party', '<h2>Our Wedding Party</h2><p>Details about the party and family</p>'),
    ('Guest Information', '<h2>Hotel Accommodations</h2><p>Hotel details/Contact no/Address</p><br><h2>Things To Do in the Area</h2><p>Tell your guests what they can do in the area.</p><br><h2>Additional information</h2><p>Tell your guests any additional information you want them to know.</p>'),
    ('Photo Album', ''), ('Music Album', ''), ('Map of Events',  ''), ('RSVP', '')])


address_dict = OrderedDict([('Ceremony' ,['Kanha Continental', 'Kanpur', 'UP', '208012']),
                            ('Reception', ['111A/102, Ashok Nagar', 'Kanpur', 'UP', '208012']),
                            ('Hotel', ['Landmark Towers', 'Kanpur', 'UP', '208012'])])




def homepage(request) :
    logged_user = request.user
    """
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())

    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    visits     = request.session['visits']
    last_visit = datetime.strftime(datetime.strptime(request.session['last_visit'][:-10], '%Y-%m-%d %I:%M'), '%b %d %Y %I:%M %p')
    """

    return render_to_response('landing_page.html', locals(), context_instance=RequestContext(request))




def contact_thanks(request) :
    return render_to_response('contact_thanks.html', context_instance=RequestContext(request))




def about_us(request) :
    logged_user = request.user
    return render_to_response('about.html', locals(), context_instance=RequestContext(request))




@login_required
def user_profile(request):
    if Wedding.objects.filter(user__username=request.user.username).exists() :
        return HttpResponseRedirect(reverse("page_list", kwargs={"username" : request.user.username}))
    else :
        return HttpResponseRedirect(reverse('profile_form', kwargs={"username" : request.user.username}))




class ThemeFormView(FormView):

    template_name = 'themes/select_theme.html'
    form_class    = ThemeForm

    def get_success_url(self):
        return reverse("page_list", kwargs={"username" : self.request.user})

    def get_context_data(self, **kwargs):
        context = super(ThemeFormView, self).get_context_data(**kwargs)
        logged_user = self.request.user
        username    = self.kwargs['username']
        context['username']  = username
        context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        if logged_user.is_authenticated :
            context['logged_user'] = logged_user

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if not Theme.objects.filter(user=self.request.user).exists() :
            Theme.objects.create(user=self.request.user,
                name=form.cleaned_data['name'])
        else :
            Theme.objects.all().update(user=self.request.user,
                name=form.cleaned_data['name'])

        return super(ThemeFormView, self).form_valid(form)




'''
class SiteAccessFormView(CookieMixin, FormView):

    template_name = 'site_access.html'
    form_class    = SiteAccessForm

    def get_success_url(self):
        username    = self.kwargs['username']
        page_slug = Page.objects.filter(user__username=username)[1].slug
        return reverse("page_detail", kwargs={"username" : str(username), "slug": str(page_slug)})

    def get_context_data(self, **kwargs):
        context = super(SiteAccessFormView, self).get_context_data(**kwargs)
        logged_user = self.request.user
        username    = self.kwargs['username']
        context['username']   = username
        context['access_key'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['access_key']
        context['page_slug']  = Page.objects.filter(user__username=username)[1].slug
        context['site_url']   = Site.objects.get_current()

        if logged_user.is_authenticated :
            context['logged_user'] = str(logged_user)

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            logged_user = self.request.user
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                error = "Incorrect Access Key provided. Try again !!"
                return render_to_response('site_access.html', {'form' : form,
                    'error' : error, 'logged_user' : str(logged_user),
                    'username' : str(username)},
                        context_instance=RequestContext(request))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.add_cookie('access_granted', 'True', max_age=3600)
        return super(SiteAccessFormView, self).form_valid(form)
'''




class HomePageFormView(FormView):

    template_name = 'wedding.html'
    form_class = WeddingForm

    def get_success_url(self):
        domain = UserProfile.objects.filter(user__username=self.kwargs['username'])
        #user_domain = domain.values().get(user=self.request.user)['user_domain']
        return reverse("page_list", kwargs={"username" : self.request.user})

    def get_context_data(self, **kwargs):
        context = super(HomePageFormView, self).get_context_data(**kwargs)
        wedding_objects = Wedding.objects.filter(user=self.request.user)
        context['wedding_objects'] = wedding_objects
        context['logged_user'] = self.request.user
        context['username'] = self.request.user.username
        context['access_key'] = \
            UserProfile.objects.filter(user__username=context['username']).values()[0]['access_key']
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        access_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
        if not Wedding.objects.filter(user=self.request.user).exists() :
            Wedding.objects.create(user=self.request.user,
                groom_first_name=form.cleaned_data['groom_first_name'],
                groom_last_name=form.cleaned_data['groom_last_name'],
                bride_first_name=form.cleaned_data['bride_first_name'],
                bride_last_name=form.cleaned_data['bride_last_name'],
                location=form.cleaned_data['location'],
                wedding_date=form.cleaned_data['wedding_date'])
            UserProfile.objects.create(user=self.request.user, access_key=access_key)
        else :
            Wedding.objects.filter(user=self.request.user).update(user=self.request.user,
                groom_first_name=form.cleaned_data['groom_first_name'],
                groom_last_name=form.cleaned_data['groom_last_name'],
                bride_first_name=form.cleaned_data['bride_first_name'],
                bride_last_name=form.cleaned_data['bride_last_name'],
                location=form.cleaned_data['location'],
                wedding_date=form.cleaned_data['wedding_date'])

        return super(HomePageFormView, self).form_valid(form)




class PageListView(ListView) :
    model = Page

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/pages/page_list.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/pages/page_list.html'
        return [template_name]

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
        username = self.kwargs['username']
        context['username'] = username
        context['domain'] = UserProfile.objects.filter(user__username=username).values()[0]['user_domain']
        context['access_key']  = UserProfile.objects.filter(user__username=username).values()[0]['access_key']
        context['site_url']    = Site.objects.get_current()

        if self.request.user.is_authenticated :
            context['logged_user'] = self.request.user
            context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']

        wedding_objects = Wedding.objects.filter(user__username=self.kwargs['username'])
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        return context




class PageDetailView(CookieMixin, FormMixin, DetailView) :

    model = Page
    form_class = SiteAccessForm

    def get_success_url(self):
        username    = self.kwargs['username']
        return reverse("page_detail", kwargs={"username" : str(username), "slug": str(self.object.slug)})

    def get_template_names(self):
        username = self.kwargs['username']

        if Theme.objects.filter(user__username=username).exists() :
            theme_selected = Theme.objects.filter(user__username=username)
            template_name = 'themes/%s/pages/page_detail.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/pages/page_detail.html'
        return [template_name]

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
        context['domain']      = UserProfile.objects.filter(user__username=username).values()[0]['user_domain']
        context['access_key']  = UserProfile.objects.filter(user__username=username).values()[0]['access_key']
        context['site_url']    = Site.objects.get_current()

        form_class = self.get_form_class()
        form       = self.get_form(form_class)
        context['form'] = form

        if 'access_granted' in self.request.COOKIES :
            context['access_granted'] = self.request.COOKIES['access_granted']
        else :
            context['access_granted'] = 'False'

        wedding_objects = Wedding.objects.filter(user__username=self.kwargs['username'])
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        if logged_user.is_authenticated :
            context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
            context['logged_user'] = str(logged_user)

        return context


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.add_cookie('access_granted', 'True', max_age=3600)
        return super(PageDetailView, self).form_valid(form)

    def form_invalid(self, form):
        error = "Incorrect Access Key provided. Try again !!"
        return self.render_to_response(self.get_context_data(form=form, error=error))

    def render_to_response(self, context, **response_kwargs):
        response = super(PageDetailView, self).render_to_response(context, **response_kwargs)
        if 'access_granted' not in self.request.COOKIES :
            response.set_cookie("access_granted", "False")
        return response




class PageUpdateView(UpdateView) :
    model = Page
    form_class = PageForm

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/pages/page_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/pages/page_form.html'
        return [template_name]

    def get_queryset(self) :
        queryset = Page.objects.filter(user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("page_detail", kwargs={"username" : str(self.request.user), "slug": str(self.object.slug)})

    def get_context_data(self, **kwargs):
        context = super(PageUpdateView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        if self.request.user.is_authenticated :
            context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context




class PhotoCreateView(CreateView):
    model = PhotoContent
    form_class = PhotoForm

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/photologue/photo_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/photologue/photo_form.html'
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(PhotoCreateView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        if self.request.user.is_authenticated :
            context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        if self.request.FILES.get('image') :
            f = form.save(commit=False)
            f.user = self.request.user
            f.slug = slugify(f.title)
            f.save()
        isvalid = super(PhotoCreateView, self).form_valid(form)
        return isvalid

    def get_success_url(self):
        return reverse('photo_list', kwargs={"username" : str(self.request.user)} )




class GalleryListView(CookieMixin, FormMixin, PhotoListView) :
    model = PhotoContent
    form_class = SiteAccessForm
    paginate_by = 20

    def get_success_url(self):
        username    = self.kwargs['username']
        return reverse("photo_list", kwargs={"username" : str(username)})

    def get_template_names(self):
        username = self.kwargs['username']
        if Theme.objects.filter(user__username=username).exists() :
            theme_selected = Theme.objects.filter(user__username=username)
            template_name = 'themes/%s/photologue/photo_list.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/photologue/photo_list.html'
        return [template_name]

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
        context['access_key']  = UserProfile.objects.filter(user__username=username).values()[0]['access_key']
        context['site_url']    = Site.objects.get_current()

        form_class = self.get_form_class()
        form       = self.get_form(form_class)
        context['form'] = form

        if 'access_granted' in self.request.COOKIES :
            context['access_granted'] = self.request.COOKIES['access_granted']
        else :
            context['access_granted'] = 'False'

        wedding_objects = Wedding.objects.filter(user__username=username)
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        context['username']        = username

        if logged_user.is_authenticated :
            context['logged_user']     = str(logged_user)
            context['is_member']       = UserProfile.objects.filter(user__username=username).values()[0]['member']

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.add_cookie('access_granted', 'True', max_age=3600)
        return super(GalleryListView, self).form_valid(form)

    def form_invalid(self, form):
        error = "Incorrect Access Key provided. Try again !!"
        return self.render_to_response(self.get_context_data(form=form, error=error))

    def render_to_response(self, context, **response_kwargs):
        response = super(GalleryListView, self).render_to_response(context, **response_kwargs)
        if 'access_granted' not in self.request.COOKIES :
            response.set_cookie("access_granted", "False")
        return response




class GalleryDetailView(CookieMixin, FormMixin, PhotoDetailView) :

    model = PhotoContent
    form_class = SiteAccessForm

    def get_success_url(self):
        username    = self.kwargs['username']
        return reverse("photo_detail", kwargs={"username" : str(username), "pk" : self.object.pk})

    def get_template_names(self):
        username = self.kwargs['username']
        if Theme.objects.filter(user__username=username).exists() :
            theme_selected = Theme.objects.filter(user__username=username)
            template_name = 'themes/%s/photologue/photo_detail.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/photologue/photo_detail.html'
        return [template_name]

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
        context['access_key']  = UserProfile.objects.filter(user__username=username).values()[0]['access_key']
        context['site_url']    = Site.objects.get_current()

        form_class = self.get_form_class()
        form       = self.get_form(form_class)
        context['form'] = form

        if 'access_granted' in self.request.COOKIES :
            context['access_granted'] = self.request.COOKIES['access_granted']
        else :
            context['access_granted'] = 'False'

        wedding_objects = Wedding.objects.filter(user__username=username)
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        context['username']        = username

        if logged_user.is_authenticated :
            context['is_member']       = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
            context['logged_user']     = str(logged_user)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.add_cookie('access_granted', 'True', max_age=3600)
        return super(GalleryDetailView, self).form_valid(form)

    def form_invalid(self, form):
        error = "Incorrect Access Key provided. Try again !!"
        return self.render_to_response(self.get_context_data(form=form, error=error))

    def render_to_response(self, context, **response_kwargs):
        response = super(GalleryDetailView, self).render_to_response(context, **response_kwargs)
        if 'access_granted' not in self.request.COOKIES :
            response.set_cookie("access_granted", "False")
        return response





class PhotoUpdateView(UpdateView) :
    model = PhotoContent
    form_class = PhotoForm

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/photologue/photo_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/photologue/photo_form.html'
        return [template_name]

    def get_queryset(self) :
        queryset = PhotoContent.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhotoUpdateView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        if self.request.user.is_authenticated :
            context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('photo_list', kwargs={"username" : str(self.request.user)} )

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.slug = slugify(f.title)
        f.save()
        isvalid = super(PhotoUpdateView, self).form_valid(form)
        return isvalid




class PhotoDeleteView(DeleteView) :
    model = PhotoContent
    #success_url = reverse_lazy('photo_list', kwargs={"username" : str(request.user)})

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/photologue/photo_confirm_delete.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/photologue/photo_confirm_delete.html'
        return [template_name]

    def get_queryset(self) :
        queryset = PhotoContent.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhotoDeleteView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        context['username'] = self.kwargs['username']

        if self.request.user.is_authenticated :
            context['is_member'] = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self) :
        return reverse('photo_list', kwargs={"username" : str(self.request.user)})





class AddressListView(CookieMixin, FormMixin, ListView) :

    model = Address
    form_class = SiteAccessForm

    def get_success_url(self):
        username    = self.kwargs['username']
        return reverse("events_list", kwargs={"username" : str(username)})

    def get_template_names(self):
        username = self.kwargs['username']
        if Theme.objects.filter(user__username=username).exists() :
            theme_selected = Theme.objects.filter(user__username=username)
            template_name = 'themes/%s/pages/address_list.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/pages/address_list.html'
        return [template_name]

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

        context['page_list']  = Page.objects.filter(user__username=username)
        context['access_key'] = UserProfile.objects.filter(user__username=username).values()[0]['access_key']
        context['site_url']   = Site.objects.get_current()

        form_class = self.get_form_class()
        form       = self.get_form(form_class)
        context['form'] = form

        if 'access_granted' in self.request.COOKIES :
            context['access_granted'] = self.request.COOKIES['access_granted']
        else :
            context['access_granted'] = 'False'

        g=geocoders.GoogleV3()
        event_address = Address.objects.filter(user__username=username)
        events = []
        addresses = []
        map_addresses = []
        for ea in event_address :
            events.append(str(ea).split(':')[0])
            addresses.append(str(ea).split(':')[1])
            map_addresses.append(g.geocode(str(ea).split(':')[1])[1])

        context['map_of_events'] = zip(events, addresses, map_addresses, event_address)

        wedding_objects = Wedding.objects.filter(user__username=username)
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        context['username']  = username

        if logged_user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
            context['logged_user'] = str(logged_user)

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.add_cookie('access_granted', 'True', max_age=3600)
        return super(AddressListView, self).form_valid(form)

    def form_invalid(self, form):
        error = "Incorrect Access Key provided. Try again !!"
        return self.render_to_response(self.get_context_data(form=form, error=error))

    def render_to_response(self, context, **response_kwargs):
        response = super(AddressListView, self).render_to_response(context, **response_kwargs)
        if 'access_granted' not in self.request.COOKIES :
            response.set_cookie("access_granted", "False")
        return response




class AddressUpdateView(UpdateView) :
    model = Address
    form_class = AddressForm

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/pages/address_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/pages/address_form.html'
        return [template_name]

    def get_queryset(self) :
        queryset = Address.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        if self.request.user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self) :
        return reverse('events_list', kwargs={"username" : str(self.request.user)})




def rsvp_thanks(request, username) :
    wedding_objects = Wedding.objects.filter(user__username=username)
    all_objects     = Page.objects.filter(user__username=username)

    if request.user.is_authenticated() :
        logged_user = str(request.user)

    response = render_to_response('pages/thanks.html',locals(), context_instance=RequestContext(request))

    if 'access_granted' not in request.COOKIES :
        response.set_cookie("access_granted", "False")
    else :
        access_granted = request.COOKIES['access_granted']

    return response




class RsvpFormView(CookieMixin, FormView):

    form_class = RsvpForm

    def get_template_names(self):
        username = self.kwargs['username']
        if Theme.objects.filter(user__username=username).exists() :
            theme_selected = Theme.objects.filter(user__username=username)
            template_name = 'themes/%s/pages/rsvp_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/pages/rsvp_form.html'
        return [template_name]

    def get_success_url(self):
        return reverse("rsvp_thanks", kwargs={"username" : self.kwargs['username']})

    def get_context_data(self, **kwargs):
        context = super(RsvpFormView, self).get_context_data(**kwargs)
        logged_user = self.request.user
        username    = self.kwargs['username']

        context['wedding_objects'] = Wedding.objects.filter(user__username=username)
        context['username']        = username

        context['access_key']  = UserProfile.objects.filter(user__username=username).values()[0]['access_key']
        context['site_url']    = Site.objects.get_current()

        form_class = self.get_form_class()
        form       = self.get_form(form_class)
        context['form'] = form

        if 'access_granted' in self.request.COOKIES :
            context['access_granted'] = self.request.COOKIES['access_granted']
        else :
            context['access_granted'] = 'False'


        wedding_objects = Wedding.objects.filter(user__username=username)
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        context['all_objects']     = Page.objects.filter(user__username=username)

        if logged_user.is_authenticated() :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
            context['logged_user'] = str(logged_user)

        return context

    def form_valid(self, form):

        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.add_cookie('access_granted', 'True', max_age=3600)
        form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name  = form.cleaned_data['last_name']
#        contact    = form.cleaned_data['contact']
        email      = form.cleaned_data['email']
#        connect    = form.cleaned_data['connect']
        response   = form.cleaned_data['response']
        username   = self.kwargs['username']
        user_email = EmailAddress.objects.get(user__username=username).email
        wedding_objects = Wedding.objects.filter(user__username=username)
        groom_name = wedding_objects.values()[0]['groom_first_name']
        bride_name = wedding_objects.values()[0]['bride_first_name']

        rsvp_queryset = Rsvp.objects.filter(first_name=first_name, last_name=last_name, email=email)

        if rsvp_queryset.exists() :
            Rsvp.objects.update(first_name=first_name, last_name=last_name, email=email, response=response)
        else :
            form.save()

        email_format = [
            ['Name', 'Email', 'Attending'],
            ['%s %s' % (first_name, last_name) , '%s' % (email), '%s' %(response)],
        ]
        message = ''
        spacing = 2
        widths = [max(len(value) for value in column) + spacing for column in zip(*email_format)]
        for line in email_format :
            message += ''.join('%-*s' % item for item in zip(widths, line)) + '\n'

        email_message =  '''Dear %s & %s,

            The following guests have submitted an online RSVP for your wedding.

            %s''' % (groom_name, bride_name, message)

        try :
            send_mail('RSVP Update', email_message , user_email, ['sunnyarora07@gmail.com'])
        except Exception as e :
            print "Exception has occured !!", e
            raise
        return super(RsvpFormView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        #self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        error = "Incorrect Access Key provided. Try again !!"
        return self.render_to_response(self.get_context_data(form=form, error=error))

    def render_to_response(self, context, **response_kwargs):
        response = super(RsvpFormView, self).render_to_response(context, **response_kwargs)
        if 'access_granted' not in self.request.COOKIES :
            response.set_cookie("access_granted", "False")
        return response




class ContactFormView(FormView):

    template_name = 'contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse("contact_thanks")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save(commit=False)
        full_name = form.cleaned_data['full_name']
        phone_num = form.cleaned_data['phone_num']
        email     = form.cleaned_data['email']
        message   = 'Full Name : ' + full_name + '\nPhone Number : ' + phone_num + '\nEmail : ' + email + '\nMessage : '
        message   += form.cleaned_data['message']
        form.save()

        try :
            send_mail('Website Query', message , 'sunnyaroraster@gmail.com', ['sunnyaroraster@gmail.com'])
        except Exception as e :
            print "Exception has occured !!", e
            raise
        return super(ContactFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        return context




class AudioFileCreateView(CreateView):
    model = AudioFile
    form_class = AudioFileForm

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/audio/audio_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/audio/audio_form.html'
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(AudioFileCreateView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        if self.request.user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        if self.request.FILES.get('audio_file') :
            f = form.save(commit=False)
            uploaded_audio_file = str(form.cleaned_data['audio_file'])
            f.name = uploaded_audio_file.split('/')[-1].split('.')[0]
            f.user = self.request.user
            f.save()
        isvalid = super(AudioFileCreateView, self).form_valid(form)
        return isvalid

    def get_success_url(self):
        return reverse('audio_list', kwargs={"username" : str(self.request.user)} )




class AudioFileListView(CookieMixin, FormMixin, ListView) :

    model = AudioFile
    form_class = SiteAccessForm

    def get_success_url(self):
        username    = self.kwargs['username']
        return reverse("audio_list", kwargs={"username" : str(username)})

    def get_template_names(self):
        username = self.kwargs['username']
        if Theme.objects.filter(user__username=username).exists() :
            theme_selected = Theme.objects.filter(user__username=username)
            template_name = 'themes/%s/audio/audio_list.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/audio/audio_list.html'
        return [template_name]

    def get_queryset(self) :
        username    = self.kwargs['username']
        queryset = AudioFile.objects.filter(user__username=username)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AudioFileListView, self).get_context_data(**kwargs)
        username    = self.kwargs['username']
        logged_user = self.request.user

        context['page_list'] = Page.objects.filter(user__username=username)
        context['audio_objects']   = AudioFile.objects.filter(user__username=username)
        context['site_url']    = Site.objects.get_current()

        form_class = self.get_form_class()
        form       = self.get_form(form_class)
        context['form'] = form

        if 'access_granted' in self.request.COOKIES :
            context['access_granted'] = self.request.COOKIES['access_granted']
        else :
            context['access_granted'] = 'False'

        wedding_objects = Wedding.objects.filter(user__username=username)
        context['wedding_objects'] = wedding_objects
        wedding_date = wedding_objects.values()[0]['wedding_date']
        current_date = date.today()
        wedding_done = 'False'
        if wedding_date <= current_date :
            wedding_done = 'True'
        context['wedding_done'] = wedding_done

        context['username']  = username

        if logged_user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
            context['logged_user'] = str(logged_user)

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request.COOKIES.get('access_granted', 'False')

        if form.is_valid():
            user_access_key = form.cleaned_data['access_key']
            username   = self.kwargs['username']
            access_key = UserProfile.objects.filter(user__username=username).values()[0]['access_key']

            if user_access_key != access_key :
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.add_cookie('access_granted', 'True', max_age=3600)
        return super(AudioFileListView, self).form_valid(form)

    def form_invalid(self, form):
        error = "Incorrect Access Key provided. Try again !!"
        return self.render_to_response(self.get_context_data(form=form, error=error))

    def render_to_response(self, context, **response_kwargs):
        response = super(AudioFileListView, self).render_to_response(context, **response_kwargs)
        if 'access_granted' not in self.request.COOKIES :
            response.set_cookie("access_granted", "False")
        return response




class AudioFileUpdateView(UpdateView) :

    form_class = AudioFileForm

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name  = 'themes/%s/audio/audio_form.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/audio/audio_form.html'
        return [template_name]

    def get_queryset(self) :
        queryset = AudioFile.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AudioFileUpdateView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user

        if self.request.user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']

        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self) :
        return reverse('audio_list', kwargs={"username" : str(self.request.user)})




class AudioFileDeleteView(DeleteView) :
    model = AudioFile

    def get_template_names(self):
        if Theme.objects.filter(user=self.request.user).exists() :
            theme_selected = Theme.objects.filter(user=self.request.user)
            template_name = 'themes/%s/audio/audio_confirm_delete.html' % (theme_selected.values()[0]['name'])
        else :
            template_name = 'themes/default/audio/audio_confirm_delete.html'
        return [template_name]

    def get_queryset(self) :
        queryset = AudioFile.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AudioFileDeleteView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['logged_user'] = self.request.user
        if self.request.user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['all_objects'] = Page.objects.filter(user=self.request.user)
        return context

    def get_success_url(self) :
        return reverse('audio_list', kwargs={"username" : str(self.request.user)})




class PaymentFormView(FormView):

    template_name = 'payment.html'
    form_class = PaymentForm

    def get_success_url(self):
        return reverse("contact_thanks")

    def get_context_data(self, **kwargs):
        context = super(PaymentFormView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated :
            context['is_member']   = UserProfile.objects.filter(user__username=self.kwargs['username']).values()[0]['member']
        context['logged_user'] = self.request.user
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save(commit=False)
        form.save()
        return super(PaymentFormView, self).form_valid(form)