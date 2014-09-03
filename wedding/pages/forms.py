from django import forms
from .models import Page
from .models import Address, Rsvp, PhotoContent, Wedding
from tinymce.widgets import TinyMCE
from photologue.models import Photo
from localflavor.in_.forms import INStateSelect
from django.forms.extras.widgets import SelectDateWidget
from datetime import date

class WeddingForm(forms.ModelForm) :

    class Meta :
        model = Wedding
        exclude = ('user',)
        widgets = {
                    'location' : INStateSelect(),
                    'wedding_date': SelectDateWidget(years=range(2014, 2021)),
        }


class PageForm(forms.ModelForm):

    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
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