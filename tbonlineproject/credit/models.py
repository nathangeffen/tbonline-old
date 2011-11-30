"""Models to represent authors, photographers, creators and other credited people.
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

class Credit(models.Model):
    '''Person or institution who created or is the source of content.
    '''
    is_person = models.BooleanField(default=True, 
                                 verbose_name=_('Is this a person?'),  
                                 help_text=_('Check this field if this is a '
                                 'person (e.g. Thomas Hardy) as opposed to ' 
                                 'an institution (e.g. Reuters).'))
    first_names = models.CharField(blank=True, max_length=200,
                                  verbose_name=_("Person's first names"), 
                                  help_text=_('Leave blank for institutions'))
    last_name = models.CharField(max_length=200,
                                 verbose_name=_('Name of institution or '
                                 'last name of person'))
    url = models.URLField(blank=True, verify_exists=False)
    
    def __unicode__(self):
        if self.is_person and unicode(self.first_names).strip():
            return u' '.join([self.first_names, self.last_name])
        else: 
            return self.last_name 


    class Meta:
        verbose_name = _('credit')
        verbose_name_plural = _('credits')
        ordering = ['last_name', 'first_names']


class OrderedCredit(models.Model):
    """Establishes an order of authors for a content item that has one or more authors.  
    """
    credit = models.ForeignKey(Credit)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    position = models.PositiveIntegerField()
    
    def __unicode__(self):
        return unicode(self.credit)
    
    class Meta:
        unique_together = ('credit', 'content_type', 'object_id',)
        ordering = ['position',]
