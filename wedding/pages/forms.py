from django import forms
from .models import Page
from .models import Address, Rsvp, PhotoContent
from .models import Wedding, Contact, Theme
from tinymce.widgets import TinyMCE
from photologue.models import Photo
from localflavor.in_.forms import INStateSelect, INPhoneNumberField
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from audiofield.models import AudioFile
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class WeddingForm(forms.ModelForm) :

    #user_domain = forms.CharField(help_text='Choose your domain(e.g: karan-shruti, karan-and-shruti, karan-&-shruti)')
    class Meta :
        model = Wedding
        exclude = ('user',)
        widgets = {
                    'location' : INStateSelect(),
                    'wedding_date': SelectDateWidget(years=range(2014, 2021)),
        }


class PageForm(forms.ModelForm):

    body = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%', 'height': '400px'}))
    class Meta:
        model = Page
        exclude = ("user", "slug", "created",)


class PhotoForm(forms.ModelForm):

    class Meta:
        model = PhotoContent
        fields = ('image', 'title', 'caption', 'crop_from', 'tags',)


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        widgets = {
            'street': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
            'state' : INStateSelect(),
        }
        exclude = ("user",)


class RsvpForm(forms.ModelForm):

    class Meta:
        model = Rsvp
        widgets = {'response': forms.RadioSelect}


class ContactForm(forms.ModelForm):

    phone_num = INPhoneNumberField(label="Phone Number")
    class Meta:
        model = Contact
        widgets = {
            'message': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        exclude = ('created',)

class ThemeForm(forms.ModelForm):

    class Meta :
        model = Theme
        widgets = {'name': forms.RadioSelect}
        exclude = ('user',)


class AudioFileForm(forms.ModelForm):

    class Meta:
        model = AudioFile
        fields = ('audio_file',)
