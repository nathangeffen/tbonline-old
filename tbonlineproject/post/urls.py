import datetime

from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import permission_required

from models import BasicPost
from views import DateDetailPostView, DetailPostView, PostsByTagView
from feeds import LatestEntriesFeed

import settings

urlpatterns = patterns('post.views',
    url(r'^$', ListView.as_view(
                    context_object_name='posts',
                    queryset=BasicPost.objects.filter(
                            date_published__lte=datetime.datetime.now()).\
                                select_subclasses(),
                    paginate_by=settings.POSTS_PER_PAGE,
                    template_name='post/post_list.html'),name='post_list'),
    
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/$', 
        DateDetailPostView.as_view(), name='post_detail'),

    url(r'^(?P<pk>\d+)/$', 
        DetailPostView.as_view(), name='post_id_detail'),
    
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('post.change_basicpost')(DetailView.as_view(
                    context_object_name="post",
                    queryset=BasicPost.objects.select_subclasses(),
                    template_name='post/post_detail.html')), name='post_draft_detail'),

    (r'^feed/$', LatestEntriesFeed()),
    
    url(r'^tag/(?P<tag>[\"\w\" \-]+)/$', PostsByTagView.as_view(), name='post_tag_list'),

)
