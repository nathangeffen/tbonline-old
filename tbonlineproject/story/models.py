'''Models for a story that represents a collection of ordered posts.  
'''
import datetime

from django.db import models    
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from tagging.models import TaggedItem 
from credit.models import OrderedCredit 
from post.models import BasicPost
from enhancedtext.fields import EnhancedTextField


class Story(models.Model):
    '''Story model encapsulates a collection of ordered posts.
    Useful for representing a book or connected articles that need a table of
    contents.
    '''
    
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = EnhancedTextField(blank=True, default="\W")
    posts = models.ManyToManyField(BasicPost, through='OrderedPost', 
                                   blank=True, 
                                   null=True)
    authors = generic.GenericRelation(OrderedCredit, verbose_name=_('authors'), 
                                      blank=True, null=True)    
    
    date_published = models.DateTimeField(blank=True, null=True,
            help_text=_('Leave blank while this is a draft.'))
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True)

    def is_published(self):
        try: 
            if datetime.datetime.now() >= self.date_published:
                return True
            else:
                return False
        except:
            return False
    is_published.short_description = _("published")

    def get_posts(self):
        posts = [orderedpost.post for orderedpost in self.orderedpost_set.all() 
            if orderedpost.post.is_published()]
        return posts
    
    def describe(self):
        return self.description
    
    @models.permalink
    def get_absolute_url(self):
        if self.is_published():
            return ('story_detail', [str(self.date_published.year),
                               str(self.date_published.month),
                               str(self.date_published.day), 
                               self.slug 
                               ])
        else: 
            return ('draft_story', [str(self.id)],) 
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')
        ordering = ['-date_published']
    
class OrderedPost(models.Model):
    '''Through class for Story model that orders posts within a story.
    '''
    story = models.ForeignKey(Story)
    post = models.ForeignKey(BasicPost)
    position = models.PositiveIntegerField(default=0)

    @models.permalink
    def get_absolute_url(self):
        if self.story.is_published():
            return ('story_post', [str(self.story.date_published.year),
                               str(self.story.date_published.month),
                               str(self.story.date_published.day), 
                               self.story.slug,
                               str(self.post.pk) 
                               ])
        else: 
            return ('draft_story_post', [str(self.story.pk), str(self.post.pk)],) 

    def __unicode__(self):
        return unicode(self.story) + ' - ' + unicode(self.post)
    
    class Meta:
        verbose_name = _('ordered post')
        verbose_name_plural = _('ordered posts')
        ordering = ['story', 'position']