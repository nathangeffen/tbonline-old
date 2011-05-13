# Create your views here.

import datetime

from django.views.generic import ListView, DateDetailView, DetailView

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
    
    
    
