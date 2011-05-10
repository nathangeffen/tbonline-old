from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.markup.templatetags.markup import markdown

from settings import MARKDOWN_EXTENSIONS

def markdownpreview(request):
    '''Used by Markitup! editor to render the markdown for the preview button.
    '''
    data = markdown(request.POST.get('data', ''), MARKDOWN_EXTENSIONS) 
    return render_to_response( 'enhancedtext/markdownpreview.html',
                              {'preview': data,},
                              context_instance=RequestContext(request))
