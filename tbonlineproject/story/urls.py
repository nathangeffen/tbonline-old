import datetime

from django.conf.urls.defaults import *
from django.views.generic import ListView, DateDetailView, DetailView
from django.contrib.auth.decorators import permission_required

from post import settings

from models import Story

from views import StoryPostView

urlpatterns = patterns('story.views',
    url(r'^$', ListView.as_view(
                    context_object_name='stories',
                    queryset=Story.objects.filter(
                            date_published__lte=datetime.datetime.now()),
                    paginate_by=settings.POSTS_PER_PAGE),name='list_stories'),
    
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/$', 
        DateDetailView.as_view(
                    context_object_name="story",
                    date_field="date_published",
                    month_format="%m",
                    queryset=Story.objects.filter(
                            date_published__lte=datetime.datetime.now()),
                    template_name='story/story_detail.html'), name='story_detail'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[a-zA-Z0-9-_]+)/(?P<post_id>\d+)/$', 
        StoryPostView.as_view(),name='story_post'),

    
    url(r'^draft/(?P<pk>\d+)/$',
        permission_required('story.change_story')(DetailView.as_view(
                    context_object_name="story",
                    queryset=Story.objects.all(),
                    template_name='story/story_detail.html')), name='draft_story'),
                       
    
)
