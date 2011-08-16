from haystack.indexes import *
from haystack import site
from archive.models import Catalogue, Document

class CatalogueIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='last_modified')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Catalogue.objects.all()

class DocumentIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='last_modified')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Document.objects.all()


site.register(Catalogue, CatalogueIndex)
site.register(Document, DocumentIndex)
