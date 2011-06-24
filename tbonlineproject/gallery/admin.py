'''Admin interface registers Image model with admin.site. 
'''
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.forms.widgets import HiddenInput
from django.db.models import PositiveIntegerField

from credit.admin import OrderedCreditInline

from gallery.models import Gallery, Image
from archive.admin import TaggedItemInline

class ImageInline(admin.TabularInline):
    classes = ('collapse open')

    model = Gallery.images.through
    extra = 0

    raw_id_fields = ('image',)

    formfield_overrides = {
        PositiveIntegerField: {'widget': HiddenInput},
    }    
    
    sortable_field_name = 'position'
    

class GalleryAdmin(admin.ModelAdmin):
    search_fields = ('title','description',)
    list_display = ('id', 'title',)
    list_editable = ('title',)
    inlines = [TaggedItemInline, ImageInline,]
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]
    

class ImageAdmin(admin.ModelAdmin):
    search_fields = ('title','caption','description')
    list_display = ('id', 'title', 'image_thumbnail','file','date_added', 'last_modified')
    list_editable = ('title',)
    prepopulated_fields = {"slug": ("title",)}
        
    inlines = [TaggedItemInline, OrderedCreditInline, ]
    
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
