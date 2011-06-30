from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class QuestionCategory(models.Model):
    '''Each question and answer is assigned to an instance of thise model.
    '''
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('question and answer category')
        verbose_name_plural = _('question and answer categories')
        ordering = ['last_modified',]
        
class QuestionAndAnswer(models.Model):
    '''Represents one question and its answer, assigned to a category.
    '''
    category = models.ForeignKey(QuestionCategory)
    question = models.TextField()
    answer = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return self.question
    
    class Meta:
        verbose_name = _('question and answer')
        verbose_name_plural = _('questions and answers')        
        ordering = ['category', 'position',]        
