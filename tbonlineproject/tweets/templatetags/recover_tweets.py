from django import template
from django.template import Context
from django.template.loaders.app_directories import load_template_source

import tweepy

import settings
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
            if settings.TWEETS_ACTIVATED:
                t = template.loader.get_template('tweets_div.html')
                accounts = TwitterUsername.objects.all()
                tweets = []
                for account in accounts:
                    base_query_string = 'from:%s' % (account.username)
                    hashtags = account.hashtag_set.all()
                    if len(hashtags) > 0:
                        query_string = '%s AND ' % (base_query_string)
                        for index, hashtag in enumerate(hashtags):
                            if hashtag.tag == '':                                           
                                query_string = base_query_string
                                break
                            if index != len(hashtags) - 1:
                                query_string = '%s #%s OR ' % (query_string, hashtag.tag)
                            else:
                                query_string = '%s #%s' % (query_string, hashtag.tag)
                    base_query_string = query_string                                        #final query string
                    tweets_from_user = tweepy.api.search(q=base_query_string, rpp=100)
                    tweets.extend(tweets_from_user)
                tweets = sorted(tweets, key=lambda tweet: tweet.created_at, reverse=True)
                return t.render(Context({'tweets': tweets}, autoescape=context.autoescape))
            else:
                return ''
        except template.VariableDoesNotExist:
            return ''

register.tag('recover_tweets', do_recover_tweets)
