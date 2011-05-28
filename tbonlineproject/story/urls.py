from django.conf.urls.defaults import *

from story.views import StoryListView, StoryDetailView, StoryPostView, DraftStoryView, DraftStoryPostView
from django.contrib.auth.decorators import permission_required


urlpatterns = patterns('story.views',
    url(r'^$', StoryListView.as_view(),
                                  name='list_stories'),
    
    url(r'^(?P<pk>\d+)/$', StoryDetailView.as_view(),
                             name='story_detail'),

    url(r'^(?P<pk>\d+)/(?P<post_id>\d+)/$', 
        StoryPostView.as_view(),name='story_post'),

    
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('post.change_story')
        (DraftStoryView.as_view()), name='draft_story'),

    url(r'^draft/(?P<pk>\d+)/(?P<post_id>\d+)/$',
        permission_required('post.change_story')
        (DraftStoryPostView.as_view()), name='draft_story_post')

)
