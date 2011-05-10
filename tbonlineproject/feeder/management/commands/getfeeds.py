import sys

from django.core.management.base import BaseCommand, CommandError
from feeder.models import Feed

class Command(BaseCommand):
    args = '<slug slug ...>'
    help = 'Updates all active feeds, or specific feeds if any are specified'

    def handle(self, *args, **options):
        feeds = []
        
        if len(args):
            for feed_slug in args:
                try:
                    feeds += Feed.objects.get(slug=feed_slug)
                except Feed.DoesNotExist:
                    raise CommandError('Feed "%s" does not exist' % feed_slug)
        else:
            feeds = Feed.objects.filter(active=True)

        for feed in feeds:
            try:
                feed.set_rss_items()
            except:
                self.stdout.write('Error updating %s: %s %s\n' % (feed.slug, sys.exc_info()[0],sys.exc_info()[1]))
            else:
                self.stdout.write('Successfully updated feed "%s"\n' % feed.slug)
