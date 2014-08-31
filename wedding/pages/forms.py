from django import forms
from .models import Page
from tinymce.widgets import TinyMCE
from photologue.models import Photo

class PageForm(forms.ModelForm):

    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Page
        exclude = ("user", "slug", "created",)


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('image', 'title', 'caption', 'crop_from', 'tags',)