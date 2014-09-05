from django.contrib import admin
from .models import Page, Address, Rsvp, PhotoContent, Wedding
from settings import STATIC_URL
from localflavor.in_.forms import INStateSelect

class PageAdmin(admin.ModelAdmin) :
    class Media :
        js = ( STATIC_URL + 'tiny_mce/tiny_mce.js', STATIC_URL + 'tiny_mce/textareas.js')

    model = Page
    prepopulated_fields = {'slug': ('title',), }

class PhotoContentAdmin(admin.ModelAdmin) :
    model = PhotoContent

class WeddingAdmin(admin.ModelAdmin) :
    model = Wedding

class AddressAdmin(admin.ModelAdmin) :

    model = Address

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'state':
            kwargs['widget'] = INStateSelect()
#        if db_field.name == 'zip_code':
#            kwargs['widget'] = INZipCodeField()

        return super(AddressAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class RsvpAdmin(admin.ModelAdmin) :

    model = Rsvp
    list_display = ['first_name', 'last_name']

admin.site.register(Page, PageAdmin)
admin.site.register(PhotoContent, PhotoContentAdmin)
admin.site.register(Wedding, WeddingAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Rsvp, RsvpAdmin)