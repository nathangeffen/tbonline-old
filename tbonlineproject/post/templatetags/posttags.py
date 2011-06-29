import re

from django import template

from post.models import BasicPost
from feeder.models import Feed 

register = template.Library()


class PostsByCategory(template.Node):
    def __init__(self, categories, var_name):
        self.categories = categories
        self.var_name = var_name

    def render(self, context):
        try:
            context[self.var_name] =  BasicPost.get_posts_by_categories(self.categories)
        except:
            pass
        return ""

def do_get_posts_by_categories(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        template_tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'(\"\w+\") as (\w+)', arg)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % template_tag_name)
    
    tags, var_name = m.groups()
    return PostsByCategory(tags[1:-1], var_name)

register.tag('get_posts_by_categories', do_get_posts_by_categories)



class PostsByTagsUnion(template.Node):
    
    def __init__(self, tags, var_name):
        self.tags = tags
        self.var_name = var_name

    def render(self, context):
        try:
            context[self.var_name] =  sorted(BasicPost.get_posts_by_tags_union(self.tags), 
                      key=lambda p: p.date_published, reverse=True)
        except:
            pass
        return ""
        
    

def do_get_posts_by_tags_union(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        template_tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'(\"\w+\") as (\w+)', arg)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % template_tag_name)
    
    tags, var_name = m.groups()
    return PostsByTagsUnion(tags[1:-1], var_name)

register.tag('get_posts_by_tags_union', do_get_posts_by_tags_union)


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

    
