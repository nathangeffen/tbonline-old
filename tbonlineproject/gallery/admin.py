'''Admin interface registers Image model with admin.site. 
'''
from django.contrib import admin
from django.contrib.contenttypes import generic

from credit.admin import OrderedCreditInline

from models import Gallery, Image

class GalleryAdmin(admin.ModelAdmin):
    search_fields = ('title','description',)
    list_display = ('id', 'title',)
    list_editable = ('title',)
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
        
    inlines = [OrderedCreditInline, ]
    
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
