''' Model definitions for content posts. 

The main content type is a BasicPost. Posts with images, slideshows and 
embedded objects inherit from BasicPost and are implemented in PostWithImage,
PostWithSlideShow and PostWithEmbeddedObject respectively.  

The 3rd party library model_utils handles getting inherited models from the 
database. A manager for BasicPost, using model_utils, is implemented in the 
PostManager class.

The query syntax for obtaining posts using this structure is quite simple: 

To get all posts, but with all their types as BasicPost (you'd seldom want to 
do this), just use the standard Django:
    BasicPost.objects.all()
    
To get all posts as their correct inherited types:
    BasicPost.objects.select_subclasses()
    
    e.g.
    posts = BasicPost.objects.select_subclasses()
    print (type(posts[0])==PostWithImage)
    
    would print True, if posts[0] happens to be a PostWithImage.
    
To get all published posts as their correct inherited types:
    BasicPost.objects.published().select_subclasses()

And to get all unpublished posts with their correct inherited types:
    BasicPost.objects.unpublished().select_subclasses()

A post is published when its date_published field is non-null and <= the 
current datetime.

'''

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.sites.models import Site

from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail
from model_utils.managers import InheritanceManager 

from tagging.models import TaggedItem, Tag

from credit.utils import credit_list

from copyright.models import Copyright
from credit.models import Credit, OrderedCredit
from gallery.models import Gallery, Image
from categories.models import Category 
from enhancedtext.fields import EnhancedTextField
from post import app_settings

class PostManager(InheritanceManager):
    '''Uses model_utils 3rd party Django library to implement methods to get
    published or unpublished posts. 
    '''
    
    def published(self):
        return super(PostManager, self).get_query_set().filter(
                date_published__lte=datetime.datetime.now(), 
                    sites__id=Site.objects.get_current().id)        

    def unpublished(self):
        return super(PostManager, self).get_query_set().\
                filter(sites__id=Site.objects.get_current().id). \
                    exclude(date_published__lte=datetime.datetime.now())

class SubmittedArticle(models.Model):
    submitted_by = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'))
    object       = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = _('submitted article')
        verbose_name_plural = _('submitted articles')
        
    def __unicode__(self):
        return  _('%s [%s]' % (self.object, self.tag))
        
class BasicPost(models.Model):
    '''This is the standard post. Complex post types requiring more 
    sophisticated content should inherit from this one. 
    
    This is really the most important class in the system. Most of the system's
    functionality is built around this model.
    '''
    
    title = models.CharField(max_length=200, 
                    help_text=_("The article title should be short, no more "
                                "than seven words. It should convey the "
                                "article's essence."))  
    subtitle = models.CharField(max_length=200, blank=True,
                    help_text=_("The subtitles should also be short but it can "
                                "be a bit longer than the title. "
                                "Only use a subtitle if it adds useful "
                                "information about the content or will draw "
                                "readers to the article. Otherwise leave "
                                "blank."))
    authors = generic.GenericRelation(OrderedCredit, verbose_name=_('authors'), 
                                      blank=True, null=True)    
    teaser = EnhancedTextField(blank=True, 
            help_text=_('For display on multi-post pages.'),
            default=("\W"))
    introduction = EnhancedTextField(blank=True,
            help_text = _('Displayed on detail post page separately from the body'),
            default=("\W"))
    body = EnhancedTextField(blank=True, default=("\W"),
                help_text=_('This is the content of the article.<br>'
                            'Note: Instead of filling in the <em>teaser</em> ' 
                            'and <em>introduction</em> fields, you can use '
                            '&#60;!--endteaser--&#62; and/or '
                            '&#60;!--endintro--&#62; in this field to indicate '
                            'where the teaser and/or introduction end '
                            'respectively.'))
        
    pullout_text = models.CharField(max_length=400, blank=True,
                        help_text=_('Usually used for a nice quote that will '
                                    'be prominently displayed'))
    slug = models.SlugField(help_text=_('Used in the URL to identify the post. ' 
                                        'This field is usually filled in '
                                        'automatically by the system. The '
                                        'system will ensure it has a  unique ' 
                                        'value.<br/>'
                                        '<b>Warning:</b> If you change the '
                                        'slug after a post is published '
                                        'the link to the post will change '
                                        'and people who have bookmarked the '
                                        'old link will not find it.'))    
    homepage = models.BooleanField(default=True,
            help_text=_('Check to display this post on the home page'))
    sticky = models.BooleanField(default=False,
            help_text=_('Check to display at top of home page even when newer '
                        'posts are published.'))
    category = models.ForeignKey(Category, blank=True, null=True,
            help_text=_('Assign this post to a category. '
                        'Posts can only have one category, but multiple tags'))
    
    date_published = models.DateTimeField(blank=True, null=True,
            help_text=_('A post is published if the publication date has ' 
                        'passed. Leave blank while this is a draft.<br/>'
                        '<b>Warning:</b> If you change this '
                        'date after a post is published '
                        'the link to the post will change '
                        'and people who have bookmarked the '
                        'old link will not find it.'))
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    
    allow_comments = models.BooleanField(default=True)
           
    detail_post_template = models.CharField(max_length=200, blank=True,
            help_text=_('Use this field to indicate an alternate html template '
                        'for detail post pages. It is safe to leave this blank.'))
    list_post_template = models.CharField(max_length=200, blank=True, 
            help_text=_('Use this field to indicate an alternate html template '
                        'for list post pages. It is safe to leave this blank.'))
    detail_post_css_classes = models.CharField(max_length=200, blank=True,
            help_text=_('Use this field to indicate additional css classes for '
                        'detail post pages. Separate classes with a space. It is ' 
                        'safe to leave this blank.'))    
    list_post_css_classes = models.CharField(max_length=200, blank=True,
            help_text=_('Use this field to indicate additional css classes for '
                        'list post pages. Separate classes with a space. '
                        'It is safe to leave this blank.'))    

    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    sites = models.ManyToManyField(Site) 
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True)
    objects = PostManager()

    def __get_template__(self, template_name, list_or_detail):
        '''Determines the template name for rendering a post and returns it as 
        a string.  
        
        The default template name is the class name + list_or_detail + html 
        extension.  
        '''
        if template_name:
            return template_name
        else:
            import os
            return os.path.join(self._meta.app_label,
                self.__class__.__name__.lower() + list_or_detail + '.html')

            
    def get_post_list_template(self):
        '''Determines the post list template name and returns it as a string.
        
        A list post template renders a bunch of posts on a webpage.  
        '''
        return self.__get_template__(self.list_post_template, '_list_snippet')
    
    def get_post_detail_template(self):
        '''Determines the post detail template name and returns it as a string.
        
        A detail post template renders one post on a webpage.  
        '''
        return self.__get_template__(self.detail_post_template, '_detail_snippet')

    def get_authors(self):
        '''Uses the credit_list utility function to generate a list of authors
        as a printable string.
        '''
        return credit_list(self.authors)
        
    def get_teaser_intro_body(self):
        '''Calculates the teaser, intro and body for this post
        
        The following possibilities exist:
        Key - 0: Field not set
              t: teaser field set
              i: intro field set
              x: teaser tag set
              y: intro tag set
              
              01. 0000: No fields set - return first paragraph as intro and 
                        teaser, remainder as body
              02. t000: teaser field set - return teaser and intro as teaser, 
                        full body as body
              03. ti00: Simplest case - teaser and intro fields set. Return 
                        full body as body  
              04. tix0: Both teaser field and tag set. Teaser field overrides 
                        teaser tag.  
              05. ti0y: Both intro field and intro tag set. Intro field 
                        overrides intro tag    
              06. 0i00: Intro field set. Teaser set to intro. Body to remainder. 
              07. 0ix0: Intro field and teaser tag set. (Madness!) Body set to 
                        remainder. 
              08. 0ixy: Same as above, but intro field overrides intro tag.
              09. 00x0: Teaser tag test. Set intro to teaser and body to 
                        remainder.
              10. 00xy: Teaser and intro tags set. Body to remainder
              11. 000y: Intro tag set. Set teaser to intro and body to 
                        remainder. 
              
        '''
                
        # Simplest case - they've all been set by the user
        
        teaser = unicode(self.teaser)
        intro = unicode(self.introduction)
        body = unicode(self.body)
        
        
        if not teaser:
            # Next simplest case: They've all been set in the body using tags
            contents = body.partition('<!--endteaser-->')
            
            if contents[1]: # The <!--endteaser--> tag is used
                teaser = contents[0]
                body = contents[2] # Body comes from remainder of text

                if not intro: # Intro field not set 
                    contents = body.partition('<!--endintro-->')
                    
                    if contents[1]: # The <!--endintro--> tag has been used
                        intro = contents[0]
                        body = contents[2] # Body is remainder of text
                    else: # <!--endintro--> tag not used, so set intro to teaser
                        intro = teaser
                        
            else: # <!--endteaser--> tag not used
                if intro: # intro field has been set
                    teaser = intro
                else: # intro field has not been set - look for <!--endintro-->
                    contents = body.partition('<!--endintro-->')
                    
                    if contents[1]: # <!--endintro--> tag used
                        teaser = intro = contents[0]
                        body = contents[2] # body is remainder of text
                    else: # No intro or teaser field set and no tags - get 1st para
                        contents = body.partition('</p>')
                        
                        if not contents[1]: # Maybe it's a capital P? 
                            contents = body.partition('</P>')
                            
                        if not contents[1]: # No paragraphs! 
                            teaser = intro = contents[0]
                            body = ""
                        else:
                            teaser = intro = contents[0] + contents[1]
                            body = contents[2]    

        else: # The teaser exists
        
            if not intro: # But the intro doesn't
                contents = body.partition('<!--endintro-->')                 

                if contents[1]: # <!--endintro--> tag used
                    intro = contents[0]
                    body = contents[2]
                else: # <!--endintro--> tag not used
                    intro = teaser
                    body = contents[0]
        
        return (teaser, intro, body)
        
    def get_teaser(self):
        return self.get_teaser_intro_body()[0]
        
    def get_introduction(self):
        return self.get_teaser_intro_body()[1]

    def get_body(self):
        return self.get_teaser_intro_body()[2]

    def describe(self):
        '''Describe methods are used by several apps in the system to return a
        description of themselves. 
        
        Some templates depend on this method existing to produce sensible
        output.   
        '''
        return self.get_introduction()

    def is_published(self):
        '''A post is published if the date-time is > date_published. 
        
        This method together with the Object Manager's published() method
        violates DRY to some extent. It is critical that they stay logically in
        sync.
        '''
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
        '''Determines all the subclasses of BasicPost, even new user defined 
        ones. 
        '''
        return [rel for rel in BasicPost._meta.get_all_related_objects() 
                if isinstance(rel.field, models.OneToOneField) and 
                    issubclass(rel.field.model, BasicPost)]
    
    def get_class(self):
        '''Will return the type of self unless this is a BasicPost in which case 
        it will try to see if there's a subclass and return that. 
        
        If that fails. return BasicPost.
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

    def get_class_name(self):
        return self.get_class().__name__

    def describe_for_admin(self):
        '''Returns a string description of the type of this Post for the admin
        interface.
        '''
        return self.get_class()._meta.verbose_name
    describe_for_admin.short_description = "Type"
    describe_for_admin.allow_tags = True

    @models.permalink
    def get_admin_url(self):
        '''Ensures that if the user clicks on a Post in the admin interface,
        the correct change screen is opened for this type of Post. 
        
        For example, if the Post is a PostWithImage, then the PostWithImage
        admin change screen must open, not the BasicPost change screen. 
        '''
        cls = self.get_class() 
        return ('admin:post_'+ self.get_class().__name__.lower() +'_change', 
                    [str(self.pk)])

    def render_admin_url(self):
        '''Called from the Admin interface to generates the html to link a post
        to its correct change screen. 
        
        Works in conjunction with get_admin_url() 
        '''
        return u'<a href="'+ self.get_admin_url() + u'">'+ unicode(self.pk) + \
                u'</a>'
    
    render_admin_url.short_description = _('ID')
    render_admin_url.allow_tags = True
    render_admin_url.admin_order_field = 'id' 

    @staticmethod
    def get_posts_by_tags_union(tags):
        '''Returns all posts which contain any of the tags in the list of tags
        passed as an argument to this method.
        '''
        
        if type(tags) == str or type(tags) == unicode:
            tags = tags.rsplit(",")
        
        if type(tags) != list:
            raise TypeError("Tags is a %s. Expected tags to be a list, string"
                            " or unicode object."  % unicode(type(tags)))

        posts = []
        
        for t in tags:
            try:
                tag = Tag.objects.get(name=t)
            except Tag.DoesNotExist:    
                continue
                
            posts_for_this_tag = list(TaggedItem.objects.\
                                      get_by_model(BasicPost, tag)) 
            for cls in BasicPost.get_subclasses():
                posts_for_this_tag += list(TaggedItem.objects.\
                                           get_by_model(cls.model, tag))
                

            posts += filter(lambda p: p.is_published() and \
                Site.objects.get_current() in p.sites.all(), posts_for_this_tag)                
        
        return list(set(posts)) # Remove duplicates 

    @staticmethod
    def get_posts_by_tags_intersection(tags):
        '''Returns all posts that have all the tags in the list of tags passed
        in the argument to this method. 
        '''
        
        if type(tags) == str or type(tags) == unicode:
            tags = tags.rsplit(",")
        if type(tags) != list:
            raise TypeError("Tags is a %s. Expected tags to be a list, string"
                            " or unicode object."  % unicode(type(tags)))
        
        posts = set([])
        for i, t in enumerate(tags):
            try:
                tag = Tag.objects.get(name=t)
            except Tag.DoesNotExist:    
                continue

            posts_for_this_tag = list(TaggedItem.objects.\
                                      get_by_model(BasicPost, tag)) 
            for cls in BasicPost.get_subclasses():
                posts_for_this_tag += list(TaggedItem.objects.\
                                           get_by_model(cls.model, tag))
                
            posts_for_this_tag = set(filter(lambda p: p.is_published() and \
                        Site.objects.get_current() in \
                            p.sites.all(), posts_for_this_tag))
            
            if i > 0: 
                posts = posts & posts_for_this_tag                
            else:
                posts = posts_for_this_tag
            
        return list(posts)

    def _get_unique_slug(self):
        '''Makes slug unique, if it is not already, and returns it as a string.
        '''
        slug_unique = False
        counter = 1
        slug = self.slug
        
        while not slug_unique: 
            if self.pk:
                posts = BasicPost.objects.filter(slug=slug).\
                    exclude(pk=self.pk)
            else:                
                posts = BasicPost.objects.filter(slug=slug)
            if len(posts) == 0:
                slug_unique = True
            else:
                slug = self.slug + "-" + unicode(counter)
                counter += 1
        return slug
        
    def save(self, *args, **kwargs):
        # Make the slug unique
        self.slug = self._get_unique_slug()
        super(BasicPost, self).save(*args, **kwargs)


    @staticmethod
    def get_posts_by_categories(categories):
        '''Returns all posts which are in the given categories.
        
        Note category is a foreign key, so a post only belongs to one category. 
        Therefore there is no union or intersection operation as there is 
        for tags.  
        '''
        if type(categories) == str or type(categories) == unicode:
            categories = categories.rsplit(",")
        if type(categories) != list:
            raise TypeError("Categories is a %s. Expected tags to be a list, "
                            "string or unicode object."  % 
                            unicode(type(categories)))
        
        return BasicPost.objects.published().\
                    filter(category__name__in=categories).\
                        select_subclasses().distinct()
                        
    @staticmethod
    def get_posts_by_author(author):
        '''Returns all posts which is authored or co-authored by the author
        passed as an argument to this method.
        '''
        if type(author) == str or type(author) == unicode:
            author = int(author)
            
        if type(author) != int:
            raise TypeError("Author is a %s. Expected author to be an int, string"
                            " or unicode object." % unicode(type(author)))
              
        author = Credit.objects.get(id=author)  
        ordered_credits = OrderedCredit.objects.filter(credit=author)
        return BasicPost.objects.published().\
              filter(authors__in=ordered_credits).\
                select_subclasses().distinct()
        
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


class PostWithImage(BasicPost):
    '''All the attributes of BasicPost but also contains an image, presumably 
    for showing as a thumbprint on multi-post pages and as a full blown 
    image on detail post pages. 
    '''
    
    image = models.ForeignKey(Image, blank=True, null=True)

    def image_thumbnail(self):
        return self.image.image_thumbnail()

    def describe_for_admin(self):
        return self.image_thumbnail()
    describe_for_admin.short_description = "Type"
    describe_for_admin.allow_tags = True

    class Meta:
        verbose_name = _('post with image')
        verbose_name_plural = _('posts with images')

class PostWithSimpleImage(BasicPost):
    '''This model was added because the PostWithImage model is actually too
    complicated for most use cases. 
    
    This model adds an image, a caption and a URL link for the image to the 
    BasicPost class.  
    '''
    image = ImageField(upload_to='uploads/images/', blank=True, null=True)
    caption = models.CharField(max_length=300, blank=True,
                          help_text=_('Give the image a meaningful '
                                      'caption. You can use HTML.'))
    url = models.URLField(verify_exists=False, blank=True, 
                           help_text=_('If this has a value then the image '
                                       'will have a link to this URL.' ))
    
    def image_thumbnail(self, height=50, width=50):
        if self.image:
            im = get_thumbnail(self.image, unicode(height) + 'x' + 
                               unicode(width), crop='center', quality=99)
            return '<img src="' + im.url + '"/>'
        else:
            return ""

    def describe_for_admin(self):
        return self.image_thumbnail()
    
    describe_for_admin.short_description = "Type"
    describe_for_admin.allow_tags = True

    class Meta:
        verbose_name = _('post with simple image')
        verbose_name_plural = _('posts with simple images')
                
class PostWithSlideshow(BasicPost):
    '''Post with multiple images which can then be displayed as a slideshow.
    '''
    gallery = models.ForeignKey(Gallery, blank=True, null=True) 
    slideshow_options = models.TextField(blank=True, 
                help_text=_('Use this to set slideshow options in JSON format. ' 
                            'Leave blank for defaults.'))    
    def slideshow_thumbnail(self):
        images = self.gallery.images.all()
        if images:
            return images[0].image_thumbnail() + '<p>' + unicode(self.gallery) + '</p>'

    def describe_for_admin(self):
        return self.slideshow_thumbnail()
    describe_for_admin.short_description = "Type"
    describe_for_admin.allow_tags = True
         
    slideshow_thumbnail.allow_tags = True
    slideshow_thumbnail.short_description = _("gallery")
    
    class Meta:
        verbose_name = _('post with slideshow')
        verbose_name_plural = _('posts with slideshows')
    
class PostWithEmbeddedObject(BasicPost):
    '''Post that can display embedded objects, e.g. Youtube.
    '''
    detail_post_embedded_html = EnhancedTextField(blank=True, default="\H")
    list_post_embedded_html = EnhancedTextField(blank=True, default="\H")

    class Meta:
        verbose_name = _('post with embedded object')
        verbose_name_plural = _('posts with embedded objects')

class PostModerator(CommentModerator):
    email_notification = app_settings.EMAIL_COMMENTS
    enable_field = 'allow_comments'
    
    if app_settings.CLOSE_COMMENTS_AFTER:
        auto_close_field = 'date_published'
        close_after = app_settings.CLOSE_COMMENTS_AFTER
    else:
        auto_close_field = None
    
    if app_settings.COMMENTS_MODERATED:
        auto_moderate_field = 'date_published'
        moderate_after = app_settings.MODERATION_FREE_DAYS
    else:
        auto_moderate_field = None

    @staticmethod
    def can_comment(post_parm, user):

        if not post_parm.allow_comments:
            return 'disallowed'

        if not post_parm.date_published:
            return 'disallowed'

        if app_settings.CLOSE_COMMENTS_AFTER:
            if post_parm.date_published + \
                 datetime.timedelta(days=app_settings.CLOSE_COMMENTS_AFTER) \
                 <= datetime.datetime.now():
                return 'closed'
    
        if  app_settings.AUTHENTICATED_COMMENTS_ONLY and\
             not user.is_authenticated():
            return 'authenticate'
    
        return 'true'
        
    def allow(self, comment, content_object, request):
        if self.can_comment(content_object, request.user) != 'true':            
            return False
        else:
            return super(PostModerator,self).allow(comment, content_object, request)  
    

for p in [BasicPost, PostWithImage, PostWithSlideshow, PostWithEmbeddedObject]:
    if p not in moderator._registry:
        moderator.register(p, PostModerator)
