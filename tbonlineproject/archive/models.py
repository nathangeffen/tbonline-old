from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from filebrowser.fields import FileBrowseField

from tagging.models import TaggedItem

from credit.models import OrderedCredit
from credit.utils import credit_list
from enhancedtext.fields import EnhancedTextField

from copyright.models import Copyright

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = FileBrowseField(max_length=200, directory="documents/", blank=True, null=True)
    url = models.URLField(blank=True,
            verify_exists=False,
            verbose_name='External URL',
            help_text= _('Use this field as an alternative to uploading a file'))
    content = EnhancedTextField(blank=True,
            help_text = _('Use this field as an alternative to uploading a file or specifying a URL.'),
            default=("\W")) 
    description = EnhancedTextField(blank=True,
            help_text = _('Describe the document.'),
            default=("\W"))
    credits = generic.GenericRelation(OrderedCredit, verbose_name=_('credit',), 
                                      blank=True, null=True) 
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True) 
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def describe(self):
        return self.description
    
    @models.permalink
    def get_absolute_url(self):
        return ('document-detail', [str(self.id)])
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        ordering = ['title',]

class Catalogue(models.Model):
    title = models.CharField(max_length=200)
    description = EnhancedTextField(blank=True, default="\W")
    documents = models.ManyToManyField(Document, blank=True, null=True,
                help_text=_('Documents in this archive.'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True)
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def describe(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        return ('calalogue_view', [str(self.id)])
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('catalogue')
        verbose_name_plural = _('catalogues')
        ordering = ['title',]


    