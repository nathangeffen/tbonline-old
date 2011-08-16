from post.models import BasicPost

from haystack.indexes import SearchIndex, CharField, DateTimeField
from haystack import site


class BasicPostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return BasicPost.objects.published()


site.register(BasicPost, BasicPostIndex)
