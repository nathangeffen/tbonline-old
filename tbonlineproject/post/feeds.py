from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from post.models import BasicPost

current_site_name =  Site.objects.get_current().name

class LatestEntriesFeed(Feed):
    title = current_site_name + _(u' posts.')
    link = "/"
    description = _('New posts on ') + current_site_name 

    def items(self):
        return BasicPost.objects.published().order_by('-date_published').select_subclasses()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser
