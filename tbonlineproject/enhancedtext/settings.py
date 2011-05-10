from django.conf import settings
"""Developer definable settings for enhancedtext app
"""

#from django.conf import settings
from django.utils.translation import ugettext as _

CONTENT_FORMATS = (
    ('\P', _('Plain text')),
    ('\E', _('Plain text with URLs and line breaks')),
    ('\R', _('reStructuredText')),    
    ('\M', _('Markdown')),
    ('\T', _('Textile')),
    ('\H', _('HTML')),    
    ('\W', _('HTML editor')),  
)

#CONTENT_FORMATS = (
#    ('\P', 'Plain text'),
#    ('\E', 'Plain text with URLs and line breaks'),
#    ('\R', 'reStructuredText'),    
#    ('\M', 'Markdown'),
#    ('\T', 'Textile'),
#    ('\H', 'HTML'),    
#    ('\W','HTML editor'),  
#)


DEFAULT_FORMAT = getattr(settings, 'ENHANCEDTEXT_DEFAULT_FORMAT', 
                       CONTENT_FORMATS[0][0])

MARKDOWN_EXTENSIONS = getattr(settings, 'ENHANCEDTEXT_MARKDOWN_EXTENSIONS', 
                        'safe,abbr,tables,def_list,footnotes')

