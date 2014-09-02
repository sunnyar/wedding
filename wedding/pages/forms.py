from django import forms
from .models import Page
from .models import Address, Rsvp, PhotoContent
from tinymce.widgets import TinyMCE
from photologue.models import Photo
from localflavor.in_.forms import INStateSelect

class CoupleForm(forms.Form) :

    groom_first_name = forms.CharField(label="Groom's First Name")
    groom_last_name = forms.CharField(label="Groom's Last Name")
    bride_first_name = forms.CharField(label="Bride's First Name")
    bride_last_name = forms.CharField(label="Bride's Last Name")
    wedding_date = forms.DateField()

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

class RsvpForm(forms.ModelForm):

    class Meta:
        model = Rsvp