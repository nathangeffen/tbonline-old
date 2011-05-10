import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import DateDetailView

from post.models import BasicPost

from models import Story

class StoryPostView(DateDetailView):

    context_object_name = "story"
    template_name = "story/story_post.html"
    date_field = "date_published"
    month_format = "%m"

    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super(StoryPostView, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(BasicPost,pk=int(self.kwargs['post_id']))
        return context
