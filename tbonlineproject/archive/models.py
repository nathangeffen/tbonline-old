import datetime

from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from filebrowser.fields import FileBrowseField

from tagging.models import TaggedItem

from credit.models import OrderedCredit
from credit.utils import credit_list, credit_length
from enhancedtext.fields import EnhancedTextField

from copyright.models import Copyright

MONTH_CHOICES = (
    ('01', _('January'),),
    ('02', _('February'),),
    ('03', _('March'),),
    ('04', _('April'),),
    ('05', _('May'),),    
    ('06', _('June'),),
    ('07', _('July'),),
    ('08', _('August'),),    
    ('09', _('September'),),    
    ('10', _('October'),),    
    ('11', _('November'),),
    ('12', _('December'),),        
)

CITATION_FORMATS = (
    ('DEF', _('Default'),),
)

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
    
    source = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    
    year_published = models.PositiveSmallIntegerField(blank=True, null=True)
    month_published = models.CharField(blank=True, max_length=2, choices=MONTH_CHOICES)
    day_published = models.PositiveSmallIntegerField(blank=True, null=True)
    
    recommended_citation = models.CharField(max_length=300, blank=True,
            help_text=_("Leave blank for system to automatically generate a citation."))
    citation_format = models.CharField(max_length=3, choices=CITATION_FORMATS,
                                       default='DEF')
    
    pmid = models.IntegerField(blank=True, null=True,
            help_text=_("Enter a Public Library of Medicine identifier if there is one."))
    doi = models.CharField(max_length=50, blank=True,
            help_text=_("Enter a Digital Object Identifier if there is one. E.g. 10.1021/ac0354342"))    
    credits = generic.GenericRelation(OrderedCredit, verbose_name=_('credit',), 
                                      blank=True, null=True) 
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True) 
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def describe(self):
        return self.description
    
    def get_count_authors(self):
        return credit_length(self.credits)
    
    def get_authors(self):
        return credit_list(self.credits)
    
    def get_date_published(self):
        if not self.year_published:
            return ""
    
            
        date_published= unicode(abs(self.year_published)) 
        
        if self.month_published:
            date_published += u' ' + self.get_month_published_display()      
        
            if self.day_published:
                date_published += u' ' + unicode(self.day_published) 

        return date_published


    
    def get_citation(self):
        """Generates a citation for the document. 
        
        Currently only default citation is implemented.
        """
        if self.recommended_citation:
            return self.recommended_citation
        
        citation = ""
        
        if self.citation_format == 'DEF':
            
            # Authors, title, date, source, PMID, DOI, URL
            authors = self.get_authors()
            if authors:
                citation += self.get_authors() + u'. '
                
            citation += self.title + u'. '
             
            date_published = self.get_date_published()
            
            if date_published:
                citation += date_published + u'. '
                
            if self.source:
                citation += self.source + u'. '
            if self.publisher:
                citation += self.publisher + u'. '
    
            if self.pmid:
                citation += 'PMID: ' + unicode(self.pmid) + '. '
                
            if self.doi:
                citation += 'DOI:' + self.doi + '. '
    
            if self.url: 
                citation += self.url + u'. '
            elif self.file: 
                citation += "http://" + unicode(Site.objects.get_current()) + unicode(self.file)
            else:
                citation += "http://" + unicode(Site.objects.get_current()) + self.get_absolute_url()

        return citation
             
    def clean(self):
        '''Validates the year/month/day combination is valid. Users can omit all 
        three, but if they enter a month, they must enter a year and if they 
        enter a day, they must enter a month.  
        '''
        
        # Don't allow draft entries to have a pub_date.
        if self.year_published: 
            year = self.year_published             
            if self.month_published:
                month = int(self.month_published)
            elif self.day_published:
                raise ValidationError(_('You must enter a month if you enter a day'))
            else:
                month = 1 # For purposes of validating the year
            if self.day_published:
                day = self.day_published
            else:
                day = 1 # For purposes of validating the year/month combination
            try:
                datetime.date(year,month,day)
            except (TypeError, ValueError):
                raise ValidationError(_('The date is invalid')) 
        elif self.month_published or self.day_published:
            raise ValidationError(_('You must enter a year if you enter a month or day'))        
                          
    @models.permalink
    def get_absolute_url(self):
        return ('document-detail', [str(self.id)])
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        ordering = ['-year_published','-month_published', '-day_published']

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


    