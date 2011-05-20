# Create your views here.

import datetime

from django.views.generic import ListView, DateDetailView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.markup.templatetags.markup import markdown

from models import BasicPost, PostModerator
import settings


class PublishedFrontPagePostsView(ListView):
    context_object_name='posts'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        return BasicPost.objects.filter(
                date_published__lte=datetime.datetime.now()).\
                filter(homepage=True).\
                select_subclasses()


class DetailPostViewMixin(object):
    context_object_name = "post"
    queryset=BasicPost.objects.filter(
        date_published__lte=datetime.datetime.now()).\
        select_subclasses()
    template_name='post/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailPostViewMixin, self).get_context_data(**kwargs)
        context['comments_allowed'] = PostModerator.can_comment(context['post'], self.request.user)
        return context

    
class DetailPostView(DetailPostViewMixin, DetailView):
    pass

class DateDetailPostView(DetailPostViewMixin, DateDetailView):
    date_field = "date_published"
    month_format = "%m"
    allow_future = True

class PostsByTagView(ListView):

    context_object_name = "posts"
    paginate_by = settings.POSTS_PER_PAGE
    template_name = 'post/post_list.html'
    def get_queryset(self):
        id_list =[post.id for post in filter(lambda p: self.kwargs['tag'] in 
                        [t.tag.name for t in p.tags.all()],  
                        BasicPost.objects.select_subclasses())]
        queryset = BasicPost.objects.filter(id__in=id_list).select_subclasses()
        return queryset
    

def markdownpreview(request):
    '''Used by Markitup! editor to render the markdown for the preview button.
    '''
    data = markdown(request.POST.get('data', ''), settings.MARKDOWN_EXTENSIONS) 
    return render_to_response( 'enhancedtext/markdownpreview.html',
                              {'preview': data,},
                              context_instance=RequestContext(request))