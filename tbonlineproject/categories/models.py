from django.db import models
from enhancedtext.fields import EnhancedTextField
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Category(models.Model):
    '''Represents a category for other objects. Designed with posts in mind.
    '''
    name = models.CharField(max_length=50)
    description = EnhancedTextField(blank=True, default="\W")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')