import datetime

from post.models import BasicPost

from haystack.indexes import SearchIndex, CharField, DateTimeField
from haystack import site


class BasicPostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return BasicPost.objects.filter(date_published__lte=datetime.datetime.now()).select_subclasses()


site.register(BasicPost, BasicPostIndex)
