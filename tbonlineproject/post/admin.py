'''Admin interface for posts.
'''

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.comments.models import Comment, CommentFlag
from django.contrib.comments.admin import CommentsAdmin
from django import forms

from tagging.models import TaggedItem  

from models import BasicPost, PostWithImage

from credit.admin import OrderedCreditInline

class TaggedItemInline(generic.GenericTabularInline):
    classes = ('collapse open')
    model = TaggedItem
    extra = 0

class BasicPostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'teaser', 'body')
    list_display = ('id', 'title', 'date_published', 'is_published', 'date_added', 'last_modified')
    list_editable = ('title', 'date_published')
    list_filter = ('date_published',)
    date_hierarchy = 'date_published'
    prepopulated_fields = {"slug": ("title",)}
    inlines = [OrderedCreditInline, TaggedItemInline]
    ordering = ('-last_modified',)
    
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

class PostWithImageAdmin(BasicPostAdmin):
    list_display = ('id', 'title', 'image_thumbnail', 'date_published', 'is_published', 'date_added', 'last_modified')
    raw_id_fields = ['image',]
    related_lookup_fields = {
        'fk': ['image'],
    }    
    

    fieldsets = (
        (_('Title'), {
            'classes' : ['collapse open'],    
            'fields': ('title', 'subtitle','slug','date_published'),
        }),
        
        (_('Content'), {
         'classes' : ['collapse open',],
         'fields': ('body',)
        }),

        (_('Teaser. introduction and pullout text'), {
         'classes' : ['collapse closed',],
         'fields': ('teaser','introduction', 'pullout_text',)
        }),


        (_('Image'), {
         'classes' : ['collapse open',],
         'fields': ('image', ('single_post_width','single_post_height',), 
                    ('many_post_width','many_post_height',),)
        }),
        
        (_('Display features'), {
         'classes' : ['collapse closed',],
         'fields': ('homepage','sticky','allow_comments', 'copyright')
        }),
                 
        (_('HTML templates'), {
         'classes' : ['collapse closed',],
         'fields': ('single_post_template','many_post_template')
        }),
        
    )

class FlatPageForm(forms.ModelForm):
    model = FlatPage
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]
            
class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm 

class CustomCommentAdmin(CommentsAdmin):
    list_display = ('id', 'name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed')

admin.site.register(BasicPost, BasicPostAdmin)
admin.site.register(PostWithImage, PostWithImageAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

admin.site.unregister(Comment)
admin.site.register(Comment, CustomCommentAdmin)
admin.site.register(CommentFlag)
