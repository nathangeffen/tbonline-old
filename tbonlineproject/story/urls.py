from django.conf.urls.defaults import *

from story.views import StoryListView, StoryPostView, StoryPostRedirectView, \
    DraftStoryView, DraftStoryPostView, StoryDateDetailView, StoryRedirectView
from django.contrib.auth.decorators import permission_required


urlpatterns = patterns('story.views',
    url(r'^$', StoryListView.as_view(),
                            name='list_stories'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/$', 
        StoryDateDetailView.as_view(), name='story_detail'),
    
    url(r'^(?P<pk>\d+)/$', StoryRedirectView.as_view(),
                             name='story_id_detail'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/post/(?P<post_id>\d+)/$', 
        StoryPostView.as_view(),name='story_post'),
                       
    url(r'^(?P<pk>\d+)/post/(?P<post_id>\d+)/$', 
        StoryPostRedirectView.as_view(),name='story_post_id'),


    url(r'^draft/(?P<pk>\d+)/(?P<post_id>\d+)/$',
        permission_required('post.change_story')
        (DraftStoryPostView.as_view()), name='draft_story_post'),

    
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('post.change_story')
        (DraftStoryView.as_view()), name='draft_story'),

)
