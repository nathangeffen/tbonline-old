import datetime

from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import permission_required

from models import BasicPost
from views import DateDetailPostView, DetailPostView, PostsByTagView
from feeds import LatestEntriesFeed

import settings

urlpatterns = patterns('post.views',
                       
    # List view for all published posts
    url(r'^$', ListView.as_view(
                    context_object_name='posts',
                    queryset=BasicPost.objects.filter(
                            date_published__lte=datetime.datetime.now()).\
                                select_subclasses(),
                    paginate_by=settings.POSTS_PER_PAGE,
                    template_name='post/post_list.html'),name='post_list'),
    
    # Detail view for post by date and slug
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/$', 
        DateDetailPostView.as_view(), name='post_detail'),

    
    # Detail view for post by id
    url(r'^by_id/(?P<pk>\d+)/$', 
        DetailPostView.as_view(), name='post_id_detail'),
    
    # Detail view for unpublished post 
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('post.change_basicpost')(DetailView.as_view(
                    context_object_name="post",
                    queryset=BasicPost.objects.select_subclasses(),
                    template_name='post/post_detail.html')), name='post_draft_detail'),

    # RSS feed for posts 
    url(r'^feed/$', LatestEntriesFeed(), name='post_feed'),
    
    # List view by tag
    url(r'^tag/(?P<tag>[\"\w\" \-]+)/$', PostsByTagView.as_view(), name='post_tag_list'),


    # Preview for Markdown for enhanced text fields
    (r'^markdownpreview/$', 'markdownpreview'),
)
