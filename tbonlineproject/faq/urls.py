from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView

from faq.models import QuestionCategory, QuestionAndAnswer

urlpatterns = patterns('faq.views',
    url(r'^$', ListView.as_view(model=QuestionCategory,
                            context_object_name="questioncategory_list",),
                            name='list_faq'),
    url(r'category/(?P<pk>\d+)/$', DetailView.as_view(model=QuestionCategory,
                            context_object_name="questioncategory",),
                            name='detail_faq_category'),
)
