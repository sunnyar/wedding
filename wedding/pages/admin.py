from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin) :
    class Media :
        js = ('/static/tiny_mce/tiny_mce.js', '/static/tiny_mce/textareas.js',)

    model = Page
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Page, PageAdmin)
