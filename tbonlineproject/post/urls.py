from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required

from post.views import ListPostView, DateDetailPostView, DetailPostView, \
    PostsByTagView, DraftPostView, RedirectPostView
from post.feeds import LatestEntriesFeed

urlpatterns = patterns('post.views',
                       
    # List view for all published posts
    url(r'^$', ListPostView.as_view(),name='post_list'),
    
    # Detail view for post by date and slug
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/$', 
        DateDetailPostView.as_view(), name='post_detail'),

    
    # Detail view for post by id
    url(r'^id/(?P<pk>\d+)/$', 
        RedirectPostView.as_view(), name='post_id_detail'),
    
    # Detail view for unpublished post 
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('post.change_basicpost')
        (DraftPostView.as_view()), name='post_draft_detail'),

    # RSS feed for posts 
    url(r'^feed/$', LatestEntriesFeed(), name='post_feed'),
    
    # List view by tag
    url(r'^tag/(?P<tag>[\"\w\" \-]+)/$', PostsByTagView.as_view(), name='post_tag_list'),


    # Preview for Markdown for enhanced text fields
    (r'^markdownpreview/$', 'markdownpreview'),
)

