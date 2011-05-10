'''Currently there is no gallery. There is only an Image model.
'''

from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from filebrowser.fields import FileBrowseField
from filebrowser.settings import ADMIN_THUMBNAIL

from tagging.models import TaggedItem
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from credit.models import OrderedCredit
from credit.utils import credit_list

from copyright.models import Copyright

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True)
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def describe(self):
        return self.description
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        ordering = ['-last_modified',]

class Image(models.Model):
    title = models.CharField(max_length=200)
    gallery = models.ManyToManyField(Gallery, blank=True, null=True)
    slug = models.SlugField(unique=True)
    file = FileBrowseField(max_length=200, directory="images/", format='image', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True, verify_exists=False)
    description = models.TextField(blank=True)
    credits = generic.GenericRelation(OrderedCredit, verbose_name=_('Credit',), 
                                      blank=True, null=True)
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True) 
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
             
    def image_thumbnail(self):
        if self.file and self.file.filetype == "Image":
            return '<img src="%s" />' % self.file.url_thumbnail
        else:        
            return ""

    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"

    def get_credits(self):
        return credit_list(self.credits)

    def describe(self):
        if self.description:
            return self.description
        else:
            return self.caption

    @models.permalink
    def get_absolute_url(self):
        return ('image_view', [str(self.id)])

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ['-last_modified']
