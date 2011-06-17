from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from enhancedtext.fields import EnhancedTextField

TYPES_OF_RELATED_CONTENT = (
    ('00', _('Related articles')),
    ('05', _('Further Reading')),
    ('10', _('See also')),
    ('15', _('Source')),
    ('20', _('Reference'))
)


class Webpage(models.Model):
    """Represents manually maintained links to external web pages for display,
    say, on the front page of a website.
    """
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, 
                          verbose_name=_('URL'))
    byline = models.CharField(blank=True, max_length=200,
                    help_text=_('The institution or organisation '
                                'that produces this website. There is no '
                                'problem with leaving this blank.'))
    date = models.DateField(blank=True, null=True,
                    help_text=_('Sometimes it is useful to include the '
                                'date a blog was written. But mostly this '
                                'field will be left blank.'))
    html_A_tag_options = models.CharField(max_length=200, blank=True,
                                  help_text=_('You can put link, title and other '
                                              'HTML A tag attributes here. '
                                              'Leave blank if you are unsure.'))
    description = EnhancedTextField(blank=True, default="\W")
    date_last_edited = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['date_last_edited',]
        verbose_name = _('webpage')
        verbose_name_plural = _('webpages')


class RelatedContent(models.Model):
    '''Model for representing additional reading links that can be attached
    to articles.
    '''

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    webpage = models.ForeignKey(Webpage,
                            verbose_name=_('link'))
    category = models.CharField(max_length=2,
                                choices=TYPES_OF_RELATED_CONTENT,
                                default='05')
    position = models.PositiveIntegerField(default=0, blank=True, null=True)

    @staticmethod
    def get_related_content(model_instance=None, content_type=None, object_id=None):
        '''Returns all instances on this model which point to either the given model_instance
        or the model instance specified by content_type and object_id.
        Either pass model_instance or content_type and object_id. Don't pass both.  
        '''
        if model_instance:
            content_type = ContentType.objects.get_for_model(model_instance)
            object_id = model_instance.pk
            
        return RelatedContent.objects.filter(content_type=content_type, object_id=object_id)


    def __unicode__(self):
        return unicode(self.content_type) + u' - '  + unicode(self.webpage)

    class Meta:
        verbose_name = _("related content")
        verbose_name_plural = _("related content")
        ordering = ('content_type', 'object_id', 'category', 'position',)

