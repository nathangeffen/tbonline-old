'''Admin interface for posts.
'''

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.comments.models import Comment, CommentFlag
from django.contrib.comments.admin import CommentsAdmin
from django import forms

from django.contrib.sites.models import Site

from sorl.thumbnail.admin import AdminImageMixin

from post.models import BasicPost, PostWithImage, PostWithSlideshow, \
                        PostWithSimpleImage, PostWithEmbeddedObject, \
                        SubmittedArticle, EditorChoice

from archive.admin import TaggedItemInline

from credit.admin import OrderedCreditInline

from relatedcontent.admin import RelatedContentInline

from enhancedtext.admin import enhancedtextcss, enhancedtextjs


post_fieldsets = (
        (_('Title'), {
            'classes' : ['collapse open'],    
            'fields': ('title', 'subtitle','slug','date_published'),
        }),
        
        (_('Content'), {
         'classes' : ['collapse open',],
         'fields': ('body',)
        }),
        (_('Display features'), {
         'classes' : ['collapse open',],
         'fields': ('homepage','sticky', 'category', 'allow_comments', 'copyright')
        }),
                  
        (_('Teaser. introduction and pullout text'), {
         'classes' : ['collapse closed',],
         'fields': ('teaser','introduction', 'pullout_text',)
        }),
                 
        (_('HTML templates'), {
         'classes' : ['collapse closed',],
         'fields': (('detail_post_template','list_post_template',),
                    ('detail_post_css_classes','list_post_css_classes',))
        }),
        (_('Sites on which this post is published'), {
         'classes' : ['collapse closed',],
         'fields' : ('sites',)
        })        
    )


class BasicPostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'teaser', 'body')
    list_display = ('render_admin_url', 'title', 'describe_for_admin', 
                    'date_published', 'category', 'homepage','is_published', 
                    'date_added', 'last_modified')
    list_editable = ('title', 'date_published','category', 'homepage', )
    list_filter = ('date_published',)
    date_hierarchy = 'date_published'
    prepopulated_fields = {"slug": ("title",)}
    inlines = [OrderedCreditInline, TaggedItemInline, RelatedContentInline]
    ordering = ('-last_modified',)

    fieldsets = post_fieldsets

    def formfield_for_manytomany(self, db_field, request, **kwargs): 
        if db_field.name == 'sites':
            kwargs["initial"]  = [Site.objects.get_current()]             
        return super(BasicPostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


    
    class Media:
        css = enhancedtextcss 
        js = enhancedtextjs

class PostWithSimpleImageAdmin(AdminImageMixin, BasicPostAdmin):
    fieldsets = post_fieldsets[0:3] + \
        ((_('Image'), {
         'classes' : ['collapse open',],
         'fields': ('image', 'caption', 'url',)
        }),) + \
        post_fieldsets[3:]
        
class PostWithImageAdmin(BasicPostAdmin):
    #list_display = ('id', 'title', 'image_thumbnail', 'date_published', 'category', 'homepage','is_published', 'date_added', 'last_modified')
    raw_id_fields = ['image',]
    related_lookup_fields = {
        'fk': ['image'],
    }    
    

    fieldsets = post_fieldsets[0:3] + \
        ((_('Image'), {
         'classes' : ['collapse open',],
         'fields': ('image',)
        }),) + \
        post_fieldsets[3:]

class PostWithSlideshowAdmin(BasicPostAdmin):
    #list_display = ('id', 'title', 'slideshow_thumbnail', 'date_published', 'category', 'homepage','is_published', 'date_added', 'last_modified')
    raw_id_fields = ['gallery',]
    related_lookup_fields = {
        'fk': ['gallery'],
    }    
    

    fieldsets = post_fieldsets[0:3] + \
        ((_('Gallery to use for slideshow'), {
         'classes' : ['collapse open',],
         'fields': ('gallery', 'slideshow_options')
        }),) + \
        post_fieldsets[3:]
    
class PostWithEmbeddedObjectAdmin(BasicPostAdmin):
    
    fieldsets = post_fieldsets[0:3] + \
        ((_('Embedded object'), {
         'classes' : ['collapse open',],
         'fields': ('list_post_embedded_html', 'detail_post_embedded_html')
        }),) + \
        post_fieldsets[3:]
    

    


class FlatPageForm(forms.ModelForm):
    model = FlatPage
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]
            
class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm 


class EditorsChoiceInline(admin.StackedInline):
    model = EditorChoice
    max_num = 1
    fields = ['editors_choice']
    can_delete = False


class CustomCommentAdmin(CommentsAdmin):
    list_display = ('id', 'name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed')
    inlines = [EditorsChoiceInline]

admin.site.register(BasicPost, BasicPostAdmin)
admin.site.register(PostWithSimpleImage, PostWithSimpleImageAdmin)
admin.site.register(PostWithImage, PostWithImageAdmin)
admin.site.register(PostWithSlideshow, PostWithSlideshowAdmin)
admin.site.register(PostWithEmbeddedObject, PostWithEmbeddedObjectAdmin)
admin.site.register(SubmittedArticle)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

admin.site.unregister(Comment)
admin.site.register(Comment, CustomCommentAdmin)
admin.site.register(CommentFlag)
