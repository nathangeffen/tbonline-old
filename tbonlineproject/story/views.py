import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from post import settings
from post.models import BasicPost

from models import Story

class StoryListView(ListView):
    context_object_name = 'stories'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())

class StoryDetailView(DetailView):                                  
    context_object_name = "story"
    template_name = 'story/story_detail.html'
    
    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())


class StoryPostView(DetailView):

    context_object_name = "story"
    template_name = "story/story_post.html"

    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super(StoryPostView, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(BasicPost,pk=int(self.kwargs['post_id']))
        return context

class DraftStoryView(StoryPostView):
    
    def get_queryset(self):
        return Story.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DraftStoryView, self).get_context_data(**kwargs)

        if context['story'].date_published is None or context['story'].date_published > datetime.datetime.now():
            messages.info(self.request, _('This story is not published. You have permission to view it .'))

        return context
        

    
