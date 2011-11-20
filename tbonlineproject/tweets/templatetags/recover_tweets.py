from django import template
from django.template import Context
from django.template.loaders.app_directories import load_template_source

from tweets.models import TwitterUsername

register = template.Library()

def do_recover_tweets(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires zero arguments' % token.contents.split()[0])
    return RecoverTweetsNode()

class RecoverTweetsNode(template.Node):

    def render(self, context):
        try:
            t = template.loader.get_template('tweets_div.html')
            return t.render(Context({'twitter_usernames': TwitterUsername.objects.all()}, autoescape=context.autoescape))
        except template.VariableDoesNotExist:
            return ''

register.tag('recover_tweets', do_recover_tweets)
