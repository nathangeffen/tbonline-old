'''Creates sitemap for Story.
'''

import datetime

from django.contrib.sitemaps import Sitemap
from models import Story

class StorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.date_published
