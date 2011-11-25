# Create your views here.

import datetime

from django.contrib.auth.decorators import user_passes_test
from django.contrib.markup.templatetags.markup import markdown
from django.contrib import messages
from django.core.cache import cache 
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DateDetailView, DetailView, RedirectView

import settings

from tagging.models import TaggedItem, Tag

from categories.models import Category

from post.models import BasicPost, PostModerator

from post import app_settings


class ListPostView(ListView):
    context_object_name='posts'
    paginate_by=app_settings.POSTS_PER_PAGE
    template_name='post/post_list.html'
    
    def get_queryset(self):
        return BasicPost.objects.published().\
                select_subclasses()
    

class PostsByTagView(ListPostView):
    
    def get_queryset(self):
        return sorted(BasicPost.get_posts_by_tags_union(self.kwargs['tag']), 
                      key=lambda p: p.date_published, reverse=True)

class PostsByCategoryView(ListPostView):
    
    template_name = 'post/post_category_list.html'
    
    def get_queryset(self):
        return sorted(BasicPost.get_posts_by_categories(self.kwargs['category']), 
                      key=lambda p: p.date_published, reverse=True)

    def get_context_data(self, **kwargs):
        context = super(PostsByCategoryView, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, name=self.kwargs['category'])
        return context

class PublishedFrontPagePostsView(ListPostView):

    @method_decorator(cache_page(60 * settings.CACHE_TIME))
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(PublishedFrontPagePostsView, self).dispatch(*args, **kwargs)
        
    def get_queryset(self):
        return BasicPost.objects.published().\
                filter(homepage=True).\
                select_subclasses()

class DetailPostViewMixin(object):
    context_object_name = "post"
    template_name='post/post_detail.html'


    def get_queryset(self):
        return BasicPost.objects.published().\
                select_subclasses()
    
    def get_context_data(self, **kwargs):
        context = super(DetailPostViewMixin, self).get_context_data(**kwargs)
        context['comments_allowed'] = PostModerator.can_comment(context['post'], self.request.user)
        return context

    
class DetailPostView(DetailPostViewMixin, DetailView):
    pass


class DraftPostView(DetailPostView):

    def get_queryset(self):
        return BasicPost.objects.select_subclasses()

    def get_context_data(self, **kwargs):
        context = super(DraftPostView, self).get_context_data(**kwargs)

        if not context['post'].is_published():
            messages.info(self.request, _('This post is not published. You have permission to view it .'))

        return context
         
class RedirectPostView(RedirectView):
    query_string = True
    
    @method_decorator(cache_page(60 * settings.CACHE_TIME))
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(RedirectPostView, self).dispatch(*args, **kwargs)
    
    def get_redirect_url(self, **kwargs):
        p = get_object_or_404(BasicPost, pk=int(kwargs['pk']), date_published__lte=datetime.datetime.now())
        return reverse('post_detail', args=[str(p.date_published.year),
                               str(p.date_published.month),
                               str(p.date_published.day), 
                               p.slug 
                               ])

class DateDetailPostView(DetailPostViewMixin, DateDetailView):
    date_field = "date_published"
    month_format = "%m"

    @method_decorator(cache_page(60 * settings.CACHE_TIME))
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(DateDetailPostView, self).dispatch(*args, **kwargs)

def markdownpreview(request):
    '''Used by Markitup! editor to render the markdown for the preview button.
    '''
    data = markdown(request.POST.get('data', ''), app_settings.MARKDOWN_EXTENSIONS) 

    return render_to_response( 'enhancedtext/markdownpreview.html',
                              {'preview': data,},
                              context_instance=RequestContext(request))
                              

@user_passes_test(lambda u: u.is_superuser)
def clear_cache(request):
    cache.clear()
    return HttpResponse(unicode(_('The cache has been cleared.')))
