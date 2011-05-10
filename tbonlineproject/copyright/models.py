
from django.db import models
from django.utils.translation import ugettext_lazy as _

    
class Copyright(models.Model):
    """This class represents the different types of copyrights that 
    can be applied to an image or article.
    """
    title = models.CharField(max_length=200)
    easy_text = models.TextField(blank=True,
        help_text=_('Explanation of copyright for non-experts.'))
    legal_text = models.TextField(blank=True,
        help_text = _('Actual legal text of the copyright.'))
    html_text = models.TextField(blank=True,
        help_text = _('HTML that can be placed on web pages '
                      'of objects under this copyright. '))
    url = models.URLField(blank=True,
        verify_exists=False, 
        help_text=_('Web address for this copyright.'))

    def describe(self):
        return self.easy_text 
    
    @models.permalink
    def get_absolute_url(self):
        return ('copyright_view', [str(self.id)])

    def get_name(self):
        return self._meta.verbose_name
    
    def __unicode__(self):
        return self.title
               
    class Meta:
        ordering = ['title']    
        verbose_name = _('copyright')
        verbose_name_plural = _('copyrights')
        