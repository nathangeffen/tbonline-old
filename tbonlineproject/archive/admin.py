from django.contrib import admin
from archive.models import Catalogue, Document

from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

from tagging.models import TaggedItem, Tag  

from credit.admin import OrderedCreditInline
from enhancedtext.admin import enhancedtextcss, enhancedtextjs
from archive.forms import TagAdminForm

class TaggedItemInline(generic.GenericTabularInline):
    verbose_name = _('tag')
    verbose_name_plural = _('tags')
    classes = ('collapse open')
    model = TaggedItem
    extra = 0 

class CatalogueInline(admin.TabularInline):
    classes = ('collapse closed')
    model = Catalogue.documents.through
    extra = 0
    verbose_name = 'Catalogue'
    raw_id_fields = ['catalogue',]
    related_lookup_fields = {
        'fk': ['catalogue'],
    }    
    
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm    

class CatalogueAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'documents__title', )
    list_display = ('id', 'title', 'date_added', 'last_modified',)
    exclude = ('documents',)
    date_hierarchy = 'date_added'
    inlines = [TaggedItemInline, ]
    ordering = ('-last_modified',)

    class Media:
        css = enhancedtextcss 
        js = enhancedtextjs
    
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'file', 'url')
    list_display = ('id', 'title', 'date_added', 'last_modified',)
    list_editable = ('title',)
    date_hierarchy = 'date_added'
    inlines = [OrderedCreditInline, CatalogueInline, TaggedItemInline, ]
    ordering = ('-last_modified',)

    
    class Media:
        css = enhancedtextcss 
        js = enhancedtextjs


admin.site.register(Catalogue, CatalogueAdmin)
admin.site.register(Document, DocumentAdmin)

admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)