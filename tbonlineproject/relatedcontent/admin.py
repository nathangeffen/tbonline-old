from django.contrib import admin
from django.contrib.contenttypes import generic
from django.forms.widgets import HiddenInput
from django.db.models import PositiveIntegerField

from relatedcontent.models import RelatedContent, Webpage

class RelatedContentInline(generic.GenericTabularInline):
    classes = ('collapse closed')
    model = RelatedContent    
    raw_id_fields = ('webpage',)
    related_lookup_fields = {
        'fk': ['webpage'],
    }    

    extra = 0
    
    formfield_overrides = {
        PositiveIntegerField: {'widget': HiddenInput},
    }    
    
    sortable_field_name = 'position'

class RelatedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'category', 'position', 'webpage', )
    list_editable = ('content_type', 'object_id', 'category', 'position', 'webpage',)  

class WebpageAdmin(admin.ModelAdmin):
    search_fields = ['title', 'url',]
    list_display = ('id', 'title', 'url')
    list_editable = ('title', 'url',)

    class Media:
        css = {
               'screen': ('markitup/skins/markitup/style.css',
                          'markitup/sets/markdown/style.css',),
               } 
        
        js = [
              'markitup/jquery.min.js',
              'markitup/jquery.markitup.js',
              'markitup/sets/markdown/set.js',
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'enhancedtext/js/enhancedtextareas.js',
             ]

    
admin.site.register(RelatedContent, RelatedContentAdmin)
admin.site.register(Webpage, WebpageAdmin)