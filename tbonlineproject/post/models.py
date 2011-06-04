''' Model definitions for content posts. 

'''

import datetime

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.text import truncate_html_words
from django.core.exceptions import ObjectDoesNotExist
from model_utils.managers import InheritanceManager 


from tagging.models import TaggedItem

from credit.utils import credit_list

from copyright.models import Copyright
from credit.models import OrderedCredit
from gallery.models import Image 
from fields import EnhancedTextField, EnhancedText
import settings


class BasicPost(models.Model):
    '''Basic post that more complex posts should inherit from.
    '''
    title = models.CharField(max_length=200)  
    subtitle = models.CharField(max_length=200, blank=True)
    authors = generic.GenericRelation(OrderedCredit, verbose_name=_('authors'), 
                                      blank=True, null=True)    
    teaser = EnhancedTextField(blank=True, 
            help_text=_('For display on multi-post pages.'),
            default=("\W"))
    introduction = EnhancedTextField(blank=True,
            help_text = _('Displayed on single post page separately from the body'),
            default=("\W"))
    body = EnhancedTextField(blank=True,
            default=("\W"))
        
    pullout_text = models.CharField(max_length=400, blank=True,
                        help_text=_('Usually used for a nice quote that will '
                                    'be prominently displayed'))
    slug = models.SlugField(help_text=_('Used in the URL to identify the post.'))    
    homepage = models.BooleanField(default=True,
            help_text=_('Check to display on home page'))
    sticky = models.BooleanField(default=False,
            help_text=_('Check to display at top of home page even when newer '
                        'posts are published.'))
    
    date_published = models.DateTimeField(blank=True, null=True,
            help_text=_('Leave blank while this is a draft.'))
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    
    allow_comments = models.BooleanField(default=True)
           
    single_post_template = models.CharField(max_length=200, blank=True,
            help_text=_('Use this field to indicate an alternate html template '
                        'for single post pages. It is safe to leave this blank.'))
    many_post_template = models.CharField(max_length=200, blank=True, 
            help_text=_('Use this field to indicate an alternate html template '
                        'for multi-post pages. It is safe to leave this blank.'))    

    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True)
    objects = InheritanceManager()


    def __get_template__(self, template_name, list_or_detail):
        if template_name:
            return template_name
        else:
            import os
            return os.path.join(self._meta.app_label,
                self.__class__.__name__.lower() + list_or_detail + '.html')

            
    def get_post_list_template(self):
        return self.__get_template__(self.many_post_template, '_list_snippet')
    
    def get_post_detail_template(self):
        return self.__get_template__(self.single_post_template, '_detail_snippet')

    def get_authors(self):
        return credit_list(self.authors)
        
    def describe(self):
        if self.introduction:
            return self.introduction
        else:
            return self.teaser

    def get_teaser(self):
        if unicode(self.teaser):
            return self.teaser
        if unicode(self.introduction):
            return self.introduction

        return truncate_html_words(unicode(self.body), settings.TRUNCATE_WORDS)
        
    def get_introduction(self):
        if unicode(self.introduction):
            return self.introduction
        if unicode(self.teaser):
            return self.teaser
        return ""

    def is_published(self):
        try: 
            if datetime.datetime.now() >= self.date_published:
                return True
            else:
                return False
        except:
            return False
    is_published.short_description = _("published")
    is_published.boolean = True
    @staticmethod
    def get_subclasses():
        return [rel for rel in BasicPost._meta.get_all_related_objects() if isinstance(rel.field, models.OneToOneField) and issubclass(rel.field.model, BasicPost)]
    
    def get_class(self):
        '''Will return the type of self unless this is a BasicPost in which case 
        it will try to see if there's a subclass and return that. If that fails. return
        BasicPost.
        '''
        if isinstance(self, BasicPost):
            for cls in BasicPost.get_subclasses():
                try:
                    inst = getattr(self, cls.var_name)
                    if inst:
                        return type(inst)
                except ObjectDoesNotExist:
                    pass
            return BasicPost
        else:
            return type(self)

    @models.permalink
    def get_admin_url(self):
        cls = self.get_class() 
        return ('admin:post_'+ self.get_class().__name__.lower() +'_change', [str(self.pk)])

    def render_admin_url(self):
        return u'<a href="'+ self.get_admin_url() + u'">'+ unicode(self.pk) + u'</a>'
    
    render_admin_url.short_description = _('ID')
    render_admin_url.allow_tags = True
    render_admin_url.admin_order_field = 'id' 


    @models.permalink
    def get_absolute_url(self):
        if self.is_published():
            return ('post_detail',[str(self.date_published.year),
                               str(self.date_published.month),
                               str(self.date_published.day), 
                               str(self.slug) 
                               ])
        else: 
            return ('post_draft_detail', [str(self.id)]) 

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-sticky', '-date_published']
        unique_together = ('slug', 'date_published')

from django.contrib.comments.moderation import CommentModerator, moderator

class PostWithImage(BasicPost):
    '''All the attributes of BasicPost but also contains an image, presumably 
    for showing as a thumbprint on multi-post pages and as a full blown 
    image on single post pages. 
    '''
    
    image = models.ForeignKey(Image)
    single_post_width = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))
    single_post_height = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))
    many_post_width = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))
    many_post_height = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))

    def image_thumbnail(self):
        return self.image.image_thumbnail()
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = _("image")

    class Meta:
        verbose_name = _('post with image')
        verbose_name_plural = _('posts with images')
                
class PostWithSlideshow(BasicPost):
    '''Post with multiple images which can then be displayed as a slideshow.
    '''
    images = models.ManyToManyField(Image, through='OrderedImage') 
    single_post_width = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))    
    single_post_height = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))   
    many_post_width = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))    
    many_post_height = models.IntegerField(default=0,
                help_text=_('Leave as zero for default to be used'))    

    class Meta:
        verbose_name = _('post with slideshow')
        verbose_name_plural = _('posts with slideshows')

class OrderedImage(models.Model):
    '''Through table for ordering images for PostWithSlideShow.
    '''
    post_with_slideshow = models.ForeignKey(PostWithSlideshow)
    image = models.ForeignKey(Image)
    position = models.PositiveIntegerField()
    
    
class PostWithEmbeddedObject(models.Model):
    '''Post that can display embedded objects, e.g. Youtube.
    '''
    single_post_embedded_html = EnhancedTextField()
    many_post_embedded_html = EnhancedTextField()

    class Meta:
        verbose_name = _('post with embedded object')
        verbose_name_plural = _('posts with embedded objects')

class PostModerator(CommentModerator):
    email_notification = settings.EMAIL_COMMENTS
    enable_field = 'allow_comments'
    
    if settings.CLOSE_COMMENTS_AFTER:
        auto_close_field = 'date_published'
        close_after = settings.CLOSE_COMMENTS_AFTER
    else:
        auto_close_field = None
    
    if settings.COMMENTS_MODERATED:
        auto_moderate_field = 'date_published'
        moderate_after = settings.MODERATION_FREE_DAYS
    else:
        auto_moderate_field = None

    @staticmethod
    def can_comment(post, user):

        if not post.allow_comments:
            return 'disallowed'

        if settings.CLOSE_COMMENTS_AFTER:
            if post.date_published + \
                 datetime.timedelta(days=settings.CLOSE_COMMENTS_AFTER) \
                 <= datetime.datetime.now():
                return 'closed'
    
        if  settings.AUTHENTICATED_COMMENTS_ONLY and\
             not user.is_authenticated():
            return 'authenticate'
    
        return 'true'
        
    def allow(self, comment, content_object, request):
        if self.can_comment(content_object, request.user) != 'true':            
            return False
        else:
            return super(PostModerator,self).allow(comment, content_object, request)  
    

for Post in [BasicPost, PostWithImage, PostWithSlideshow, PostWithEmbeddedObject]:
    if Post not in moderator._registry:
        moderator.register(Post, PostModerator)
