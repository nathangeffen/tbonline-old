import datetime

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, DateDetailView, RedirectView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from post import app_settings
from post.models import BasicPost

from models import Story

class StoryListView(ListView):
    context_object_name = 'stories'
    paginate_by = app_settings.POSTS_PER_PAGE

    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())

class StoryDetailViewMixin(object):
    context_object_name = "story"
    template_name = 'story/story_detail.html'

    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())


class StoryDateDetailView(StoryDetailViewMixin, DateDetailView):
    date_field = "date_published"
    month_format = "%m"

class StoryDetailView(StoryDetailViewMixin, DetailView):                                  
    pass

class StoryRedirectView(RedirectView):
    query_string = True
    
    def get_redirect_url(self, **kwargs):
        story = get_object_or_404(Story, pk=int(kwargs['pk']), date_published__lte=datetime.datetime.now())
        return reverse('story_detail', args=[str(story.date_published.year),
                               str(story.date_published.month),
                               str(story.date_published.day), 
                               story.slug 
                               ])

class StoryPostView(DateDetailView):
    date_field = "date_published"
    month_format = "%m"
    context_object_name = "story"
    template_name = "story/story_post.html"

    def get_queryset(self):
        return Story.objects.filter(date_published__lte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super(StoryPostView, self).get_context_data(**kwargs)
        post_pk = int(self.kwargs['post_id']) 
        
        if post_pk not in [p.post.pk for p in context['story'].orderedpost_set.all()]: 
            raise Http404 
        
        context['post'] = get_object_or_404(BasicPost,pk=post_pk,date_published__lte=datetime.datetime.now())

        return context

class StoryPostRedirectView(RedirectView):
    query_string = True

    def get_redirect_url(self, **kwargs):
        story = get_object_or_404(Story, pk=int(kwargs['pk']), date_published__lte=datetime.datetime.now())

        post_pk = int(self.kwargs['post_id']) 
        
        if post_pk not in [p.post.pk for p in story.orderedpost_set.all()]: 
            raise Http404 
        
        return reverse('story_post', args=[str(story.date_published.year),
                               str(story.date_published.month),
                               str(story.date_published.day), 
                               story.slug,
                               self.kwargs['post_id']
                               ])


class DraftStoryView(StoryDetailView):
    
    def get_queryset(self):
        return Story.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DraftStoryView, self).get_context_data(**kwargs)

        if context['story'].date_published is None or context['story'].date_published > datetime.datetime.now():
            messages.info(self.request, _('This story is not published. You have permission to view it .'))

        return context
        
class DraftStoryPostView(DetailView):
    context_object_name = "story"
    template_name = "story/story_post.html"
    
    def get_queryset(self):
        return Story.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DraftStoryPostView, self).get_context_data(**kwargs)

        if context['story'].date_published is None or context['story'].date_published > datetime.datetime.now():
            messages.info(self.request, _('This story is not published. You have permission to view it .'))        

        post_pk = int(self.kwargs['post_id']) 
        
        if post_pk not in [p.post.pk for p in context['story'].orderedpost_set.all()]: 
            raise Http404 
        
        context['post'] = get_object_or_404(BasicPost,pk=post_pk)

        if context['post'].is_published() == False:
            messages.info(self.request, _('This post is not published. You have permission to view it .'))                
        
        return context
    
