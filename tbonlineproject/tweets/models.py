from django.db import models
from django.utils.translation import ugettext_lazy as _

class TwitterUsername(models.Model):
    username = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = _('Twitter Username')
        verbose_name_plural = _('Twitter Usernames')
        
    def __unicode__(self):
        return self.username
        
class Hashtag(models.Model):
    username = models.ForeignKey(TwitterUsername)
    tag = models.CharField(max_length=140, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Hashtag')
        verbose_name_plural = _('Hashtags')
        
    def __unicode__(self):
        return '%d-%s' % (self.id, self.tag)
