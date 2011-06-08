'''Creates sitemap for BasicPost and its subclasses.
'''

from django.contrib.sitemaps import Sitemap
from post.models import BasicPost

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return BasicPost.objects.published().select_subclasses()

    def lastmod(self, obj):
        return obj.date_published
