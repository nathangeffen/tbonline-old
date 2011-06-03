import re

from django import template

from models import BasicPost

register = template.Library()

class RelatedPostsRetriever(template.Node):
    
    def __init__(self, pk, var_name):
        self.id = int(pk)
        self.var_name = var_name

    def render(self, context):
        try:
            post = BasicPost.objects.filter(pk=self.pk).select_subclasses()[0]
            context[self.var_name] = TaggedItem.objects.get_by_model(BasicPost, t).select_subclasses()
        except:
            return ""
    

def do_get_related_posts(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'(\"\w+\") as (\w+)', arg)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    
    pk, var_name = m.groups()
    return RelatedPostsRetriever(pk[1:-1], var_name)

register.tag('get_related_posts', do_get_related_posts)


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

    
