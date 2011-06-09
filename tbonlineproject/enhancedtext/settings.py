from django.conf import settings

DEFAULT_FORMAT = "\W"

MARKDOWN_EXTENSIONS = getattr(settings, 'ENHANCEDTEXT_MARKDOWN_EXTENSIONS', 
                        'abbr,tables,def_list,footnotes,urlize')
