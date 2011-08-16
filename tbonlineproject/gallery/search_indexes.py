import datetime
from haystack.indexes import *
from haystack import site
from gallery.models import Gallery, Image

class GalleryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='last_modified')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Gallery.objects.all()

class ImageIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='last_modified')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Image.objects.all()


site.register(Gallery, GalleryIndex)
site.register(Image, ImageIndex)
