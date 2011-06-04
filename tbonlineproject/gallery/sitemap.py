'''Creates sitemap for galleries and images.
# TO DO: Galleries
'''

from django.contrib.sitemaps import Sitemap
from gallery.models import Image

class ImageSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Image.objects.all()

    def lastmod(self, obj):
        return obj.last_modified
