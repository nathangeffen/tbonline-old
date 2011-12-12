'''Currently there is no gallery. There is only an Image model.
'''

from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from filebrowser.fields import FileBrowseField

from tagging.models import TaggedItem

from credit.models import OrderedCredit
from credit.utils import credit_list

from enhancedtext.fields import EnhancedTextField
from copyright.models import Copyright

SIZES = (
    ('s', _('Small')),
    ('m', _('Medium')),
    ('l', _('Large'))
)

class Image(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    file = FileBrowseField(max_length=200, directory="images/", format='image', 
                           blank=True, null=True)
    preferred_size = models.CharField(max_length=1, choices=SIZES,
                        blank=True,
                        help_text=_('In some cases setting this can help HTML '
                                    'writers display the image display.'))
    caption = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True, verify_exists=False,
                verbose_name=('URL'),
                help_text=_('URL for image to link to, usually the source.'))
    description = EnhancedTextField(blank=True, default="\W")
    credits = generic.GenericRelation(OrderedCredit, verbose_name=_('Credit',), 
                                      blank=True, null=True)
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True) 
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
             
    def image_thumbnail(self):
        if self.file and self.file.filetype == "Image":
            return '<img src="%s" />' % self.file.url_thumbnail
        else:        
            return ""

    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"

    def _get_unique_slug(self):
        '''Makes slug unique, if it is not already, and returns it as a string.
        '''
        slug_unique = False
        counter = 1
        slug = self.slug
        
        while not slug_unique: 
            if self.id:
                images = Image.objects.filter(slug=slug).\
                    exclude(pk=self.id)
            else:                
                images = Image.objects.filter(slug=slug)
            if len(images) == 0:
                slug_unique = True
            else:
                slug = self.slug + "-" + unicode(counter)
                counter += 1
        return slug
        
    def get_credits(self):
        return credit_list(self.credits)

    def describe(self):
        if unicode(self.description).strip():
            return self.description
        else:
            return self.caption

    @models.permalink
    def get_absolute_url(self):
        return ('image_view', [str(self.id)])

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ['-last_modified']


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = EnhancedTextField(blank=True, default="\W")
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), 
                                      blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True, null=True, through="OrderedImage")
    copyright = models.ForeignKey(Copyright, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def describe(self):
        return self.description
    
    def get_images(self):
        return self.images.order_by('orderedimage__position')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        ordering = ['-last_modified',]

class OrderedImage(models.Model):
    gallery = models.ForeignKey(Gallery)
    image = models.ForeignKey(Image)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('ordered image')
        verbose_name_plural = _('ordered images')
        ordering = ['gallery', 'position']
        unique_together = ('gallery', 'image',)
