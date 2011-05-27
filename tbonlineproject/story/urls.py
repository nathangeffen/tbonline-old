from django.conf.urls.defaults import *

from story.views import StoryListView, StoryDetailView, StoryPostView, DraftStoryView
from django.contrib.auth.decorators import permission_required


urlpatterns = patterns('story.views',
    url(r'^$', StoryListView.as_view(),
                                  name='list_stories'),
    
    url(r'^(?P<pk>\d+)/$', StoryDetailView.as_view(),
                             name='story_detail'),

    url(r'^(?P<pk>\d+)/(?P<post_id>\d+)/$', 
        StoryPostView.as_view(),name='story_post'),

    
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('post.change_basicpost')
        (DraftStoryView.as_view()), name='draft_story')
)
