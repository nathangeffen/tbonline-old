import datetime
from haystack.indexes import *
from haystack import site
from models import BasicPost


class BasicPostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return BasicPost.objects.filter(date_published__lte=datetime.datetime.now())


site.register(BasicPost, BasicPostIndex)
