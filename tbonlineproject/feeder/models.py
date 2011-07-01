import ast
import feedparser

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Entry(models.Model):
    feed = models.ForeignKey('Feed')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(verify_exists=False)
    value = models.TextField()
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['feed', '-date_added',]
        verbose_name = _('RSS feed entry')
        verbose_name_plural = _('RSS feed entries')    

class Feed(models.Model):
    """Extremely simple model for user-specified RSS that uses Universal Feed 
    Parser library.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    url = models.URLField(verify_exists=False,
                          help_text=_('Paste the URL of the '
                                      'RSS feed here.'))
    active = models.BooleanField(default=True,
            help_text=_('If this is set, then this RSS feed will be retrieved.'))
    description = models.TextField(blank=True)
    number_of_items = models.IntegerField(default=5)    
    position = models.IntegerField(default=0, 
                                help_text=_('Determines position of this RSS feed '\
                                'relative to others.'))
    keep_old_items = models.BooleanField(default=False)        
    
    def set_rss_items(self):
        feed = feedparser.parse(self.url)
        entries = feed["items"]

        if not self.keep_old_items:
            Entry.objects.filter(feed__id=self.id).delete()

                
        if len(entries) == 0:
            return None
        else:       
            for i in range(min(len(entries)-1,self.number_of_items-1),-1,-1):
                try:
                    Entry.objects.get(link=entries[i].link)
                except Entry.DoesNotExist:
                    e = Entry()
                    e.feed = self
                    e.title = entries[i].title
                    e.link = entries[i].link
                    e.description = entries[i].description
                    e.value = unicode(entries[i])
                    e.save()
        
    def get_rss_items(self):
        entries = Entry.objects.filter(feed__id=self.id)[0:self.number_of_items]
        for e in entries: 
            try:
                e.value = ast.literal_eval(e.value)
            except:
                e.value = None
        return entries

    @models.permalink
    def get_absolute_url(self):
        return ('detailfeeder', [str(self.slug),])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['position',]
        verbose_name = _('RSS feed')
        verbose_name_plural = _('RSS feeds')
    
