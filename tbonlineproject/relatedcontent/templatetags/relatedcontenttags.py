import re

from django import template

from relatedcontent.models import RelatedContent

register = template.Library()

class RelatedContentRetriever(template.Node):
    
    def __init__(self, model_instance, var_name):
        self.model_instance = model_instance
        self.var_name = var_name

    def render(self, context):
        try:
            context[self.var_name] = RelatedContent.get_related_content(context[self.model_instance])
        except:
            pass
        return ""
    

def do_get_related_content(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, expression = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'(\w+) as (\w+)', expression)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    
    obj_name, var_name = m.groups()
    return RelatedContentRetriever(obj_name, var_name)


register.tag('get_related_content', do_get_related_content)

