'''Admin interface for stories.
'''

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.forms.widgets import HiddenInput
from django.db.models import PositiveIntegerField

from tagging.models import TaggedItem  
from post.models import BasicPost
from post.admin import TaggedItemInline
from credit.admin import OrderedCreditInline

from models import Story

class PostInline(admin.TabularInline):
    classes = ('collapse open')
    model = Story.posts.through
    raw_id_fields = ['post',]
    related_lookup_fields = {
        'fk': ['post'],
    }    
    extra = 0

    formfield_overrides = {
        PositiveIntegerField: {'widget': HiddenInput},
    }    
    
    sortable_field_name = 'position'

class StoryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description',)
    list_display = ('id', 'title', 'date_published', 'date_added', 'last_modified')
    list_editable = ('title', 'date_published')
    list_filter = ('date_published',)
    date_hierarchy = 'date_published'
    prepopulated_fields = {"slug": ("title",)}
    inlines = [OrderedCreditInline, PostInline, TaggedItemInline]
    
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]

admin.site.register(Story, StoryAdmin)

