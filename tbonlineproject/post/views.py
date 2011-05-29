# Create your views here.

import datetime

from django.views.generic import ListView, DateDetailView, DetailView, RedirectView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.markup.templatetags.markup import markdown
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from models import BasicPost, PostModerator
import settings


class ListPostView(ListView):
    context_object_name='posts'
    paginate_by=settings.POSTS_PER_PAGE
    template_name='post/post_list.html'
    
    def get_queryset(self):
        return BasicPost.objects.filter(
                date_published__lte=datetime.datetime.now()).\
                select_subclasses()
    

class PostsByTagView(ListPostView):

    def get_queryset(self):
        id_list =[post.id for post in filter(lambda p: self.kwargs['tag'] in 
                        [t.tag.name for t in p.tags.all()],  
                        BasicPost.objects.select_subclasses())]
        queryset = BasicPost.objects.filter(id__in=id_list).select_subclasses()
        return queryset
    

class PublishedFrontPagePostsView(ListPostView):

    def get_queryset(self):
        return BasicPost.objects.filter(
                date_published__lte=datetime.datetime.now()).\
                filter(homepage=True).\
                select_subclasses()


class DetailPostViewMixin(object):
    context_object_name = "post"
    template_name='post/post_detail.html'


    def get_queryset(self):
        return BasicPost.objects.filter(
                date_published__lte=datetime.datetime.now()).\
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

        if context['post'].date_published is None or context['post'].date_published > datetime.datetime.now():
            messages.info(self.request, _('This post is not published. You have permission to view it .'))

        return context
           
class RedirectPostView(RedirectView):
    query_string = True
    
    def get_redirect_url(self, **kwargs):
        post = get_object_or_404(BasicPost, pk=int(kwargs['pk']), date_published__lte=datetime.datetime.now())
        return reverse('post_detail', args=[str(post.date_published.year),
                               str(post.date_published.month),
                               str(post.date_published.day), 
                               post.slug 
                               ])


    
class DateDetailPostView(DetailPostViewMixin, DateDetailView):
    date_field = "date_published"
    month_format = "%m"

def markdownpreview(request):
    '''Used by Markitup! editor to render the markdown for the preview button.
    '''
    data = markdown(request.POST.get('data', ''), settings.MARKDOWN_EXTENSIONS) 

    return render_to_response( 'enhancedtext/markdownpreview.html',
                              {'preview': data,},
                              context_instance=RequestContext(request))
