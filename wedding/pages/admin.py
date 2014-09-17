from django.contrib import admin
from .models import Page, Address, Rsvp, PhotoContent
from audiofield.models import AudioFile
from .models import Wedding, UserProfile, Contact, Theme
from settings import STATIC_URL
from localflavor.in_.forms import INStateSelect, INPhoneNumberField
from django_summernote.admin import SummernoteModelAdmin

class AudioFileAdmin(admin.ModelAdmin) :
    model = AudioFile
    list_display = ('name', 'audio_file_player', 'user')
    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        #custom delete code
        n = queryset.count()
        for i in queryset:
            if i.audio_file:
                if os.path.exists(i.audio_file.path):
                    os.remove(i.audio_file.path)
            i.delete()
        self.message_user(request, _("Successfully deleted %d audio files.") % n)
    custom_delete_selected.short_description = "Delete selected items"

    def get_actions(self, request):
        actions = super(AudioFileAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class PageAdmin(SummernoteModelAdmin) :
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


class UserProfileAdmin(admin.ModelAdmin) :

    model = UserProfile


class ContactAdmin(admin.ModelAdmin) :

    model = Contact
    list_display = ('full_name', 'email', 'created',)
    ordering = ['-created']


class ThemeAdmin(admin.ModelAdmin) :

    model = Theme
    list_display = ('user', 'name',)


admin.site.register(Page, PageAdmin)
admin.site.register(PhotoContent, PhotoContentAdmin)
admin.site.register(Wedding, WeddingAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Rsvp, RsvpAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Theme, ThemeAdmin)