import re

from django import template
from feeder.models import Feed


register = template.Library()

class SingleFeedRetriever(template.Node):
    
    def __init__(self, slug, var_name):
        self.slug = slug
        self.var_name = var_name

    def render(self, context):
        try:
            context[self.var_name] = Feed.objects.get(slug=self.slug) 
        except Feed.DoesNotExist:
            pass
        return ""


def do_get_feeder(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'(\"[a-zA-Z0-9_-]+\") as (\w+)', arg)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    
    slug, var_name = m.groups()
    return SingleFeedRetriever(slug[1:-1], var_name)

register.tag('get_feeder', do_get_feeder)


class AllFeedRetriever(template.Node):
    
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Feed.objects.filter(active=True)
        if len(context[self.var_name]) == 0:
            return ""


def do_get_active_feeders(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'as (\w+)', arg)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    
    var_name = m.groups()[0]
    
    return AllFeedRetriever(var_name)

register.tag('get_active_feeders', do_get_active_feeders)

