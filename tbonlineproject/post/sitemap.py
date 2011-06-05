'''Creates sitemap for BasicPost and its subclasses.
'''

import datetime

from django.contrib.sitemaps import Sitemap
from models import BasicPost

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return BasicPost.objects.select_subclasses().filter(date_published__lte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.date_published
