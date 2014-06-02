import re

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from tagging.models import Tag

from post.models import BasicPost, EditorChoice, PostWithImage
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

def get_tag_cloud():
    cloud = Tag.objects.cloud_for_model(BasicPost) + Tag.objects.cloud_for_model(PostWithImage)
    sorted(cloud, key=lambda c: c.name)
    return {"tags" : cloud}

register.inclusion_tag('tag_cloud.html')(get_tag_cloud)

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


def get_comments(post, editors_choice):
    model_name = post.get_class_name().lower()
    content_type = ContentType.objects.get(app_label="post",
                                           model=model_name)

    post_comments = Comment.objects.filter(content_type=content_type,
                                           object_pk=post.id)

    choice = EditorChoice.objects.filter(editors_choice=True)\
                     .values('comment')
    choice_ids = [x['comment'] for x in choice]
    if editors_choice:
        return post_comments.filter(id__in=choice_ids)
    else:
        return post_comments.exclude(id__in=choice_ids)


def get_choice_comments(post):
    return get_comments(post, editors_choice=True)

def get_normal_comments(post):
    return get_comments(post, editors_choice=False)

register.filter('get_choice_comments', get_choice_comments)
register.filter('get_normal_comments', get_normal_comments)

