# Create your views here.

import datetime
import os

from django.contrib.auth.decorators import user_passes_test
from django.contrib.markup.templatetags.markup import markdown
from django.contrib import messages
from django.core.cache import cache 
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DateDetailView, DetailView, RedirectView

import settings

from tagging.models import TaggedItem, Tag

from categories.models import Category
from credit.models import Credit, OrderedCredit
from enhancedtext.fields import EnhancedText
from gallery.models import Gallery, Image, OrderedImage
from post.forms import ArticleSubmissionForm, ImageForm
from post.models import BasicPost, PostWithSimpleImage, PostWithSlideshow, \
                            PostModerator, SubmittedArticle

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
        
class PostsByAuthorView(ListPostView):
    
    template_name = 'post/post_author_list.html'
    
    def get_queryset(self):
        return sorted(BasicPost.get_posts_by_author(self.kwargs['author']),
                      key=lambda p: p.date_published, reverse=True)
                      
    def get_context_data(self, **kwargs):
        context = super(PostsByAuthorView, self).get_context_data(**kwargs)
        context['author'] = get_object_or_404(Credit, id=self.kwargs['author'])
        return context

class SubmittedArticleListView(ListView):
    context_object_name= 'articles'
    paginate_by=app_settings.POSTS_PER_PAGE
    template_name = 'submit_article/list.html'
    
    def get_queryset(self):
        user = self.request.user
        submitted_articles = SubmittedArticle.objects.filter(submitted_by=user).order_by('-submitted_on')
        unpublished_articles = []
        for article in submitted_articles:
            if not article.object.is_published():
                unpublished_articles.append(article)
        return unpublished_articles
        
class PublishedFrontPagePostsView(ListPostView):

    def dispatch(self, *args, **kwargs):
        return super(PublishedFrontPagePostsView, self).dispatch(*args, **kwargs)
       
    def get(self, *args, **kwargs):
        return super(PublishedFrontPagePostsView, self).get(*args, **kwargs)
        
    def post(self, *args, **kwargs):
        return super(PublishedFrontPagePostsView, self).post(*args, **kwargs)
        
    def get_queryset(self):
        return BasicPost.objects.published().\
                filter(homepage=True).\
                select_subclasses()
                
    def get_context_data(self, **kwargs):
        cache_value = cache.get('context_frontpage', '')
        if cache_value == '':
            context = super(PublishedFrontPagePostsView, self).get_context_data(**kwargs)
            cache.add('context_frontpage', context, 60 * settings.CACHE_TIME)
        else:
            context = cache.get('context_frontpage')
        return context

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
    
    def dispatch(self, *args, **kwargs):
        return super(RedirectPostView, self).dispatch(*args, **kwargs)
  
    def get(self, *args, **kwargs):
        return super(RedirectPostView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return super(RedirectPostView, self).post(*args, **kwargs)
    
    def get_redirect_url(self, **kwargs):
        p = get_object_or_404(BasicPost, pk=int(kwargs['pk']), date_published__lte=datetime.datetime.now())
        return reverse('post_detail', args=[str(p.date_published.year),
                               str(p.date_published.month),
                               str(p.date_published.day), 
                               p.slug 
                               ])
                               
    def get_context_data(self, **kwargs):
        cache_value = cache.get('context', '')
        if cache_value == '':
            context = super(RedirectPostView, self).get_context_data(**kwargs)
            cache.add('context', context, 60 * settings.CACHE_TIME)
        else:
            context = cache.get('context')
        return context

class DateDetailPostView(DetailPostViewMixin, DateDetailView):
    date_field = "date_published"
    month_format = "%m"

    def dispatch(self, *args, **kwargs):
        return super(DateDetailPostView, self).dispatch(*args, **kwargs)
       
    def get(self, *args, **kwargs):
        return super(DateDetailPostView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return super(DateDetailPostView, self).post(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        post =  kwargs['object']
        cache_key = 'context_%s_%s' % (post.get_class_name(), post.id)
        cache_value = cache.get(cache_key, '')

        if cache_value == '':
            context = super(DateDetailPostView, self).get_context_data(**kwargs)
            cache.add(cache_key, context, 60 * settings.CACHE_TIME)
        else:
            context = cache.get(cache_key)
        return context
        
def markdownpreview(request):
    '''Used by Markitup! editor to render the markdown for the preview button.
    '''
    data = markdown(request.POST.get('data', ''), app_settings.MARKDOWN_EXTENSIONS) 

    return render_to_response( 'enhancedtext/markdownpreview.html',
                              {'preview': data,},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.has_perm('post.can_submit'))                            
def submit_article(request):
    '''
        View for Article Submission
    '''
    ImageFormset = formset_factory(ImageForm, extra=settings.MAX_NUM_IMAGES)
    if request.method == 'POST':
        form = ArticleSubmissionForm(request.POST, request.FILES)
        image_forms = ImageFormset(request.POST, request.FILES)
        if form.is_valid() and image_forms.is_valid():
            title = request.POST['title']
            subtitle = request.POST['subtitle']
            body = request.POST['body']
            editor = request.POST['editor']
            authors = request.POST.get('authors', [])
            tags = request.POST.get('tags', [])
            files = request.FILES
            post_body = EnhancedText(body, editor)                                  #Combines body and editor field to for creating post
            post = None
            if len(files) == 0:                                                     #Will save post as basic post
                post = BasicPost(title=title, slug=slugify(title), 
                                    subtitle=subtitle, body=post_body)
                post.slug = post._get_unique_slug()
                post.save()
            elif len(files) == 1:                                                   #Will save post as post with simple image
                image = None
                image = files.itervalues().next()
                post = PostWithSimpleImage(title=title, slug=slugify(title),
                                            subtitle=subtitle, body=post_body,
                                            image=image)
                post.save()
            else:                                                                   #Will save post as post with slideshow
                gallery = Gallery(title=title)
                gallery.save()
                path = os.path.join(settings.MEDIA_ROOT, 'uploads')
                path = os.path.join(path, 'images')
                for index, image in enumerate(files):
                    filename_unique = False
                    filename = os.path.join(path, files[image].name)
                    counter = 1
                    while not filename_unique:
                        if os.path.exists(filename):
                            filename_split = filename.split('.')
                            filename = filename_split[0]
                            extension = filename_split[1]
                            filename = filename + unicode(counter) + '.' + extension
                        else:
                            filename_unique = True
                    image_file = open(filename, 'wb+')
                    for chunk in files[image].chunks():
                        image_file.write(chunk)
                    image_file.close()
                    filename_split = filename.split(os.sep) 
                    base_filename = filename_split[-1]
                    filename = os.path.join('uploads', 'images')
                    filename = os.path.join(filename, base_filename)
                    image = Image(title=title, slug=slugify(title), file=filename)
                    image.slug = image._get_unique_slug()
                    image.save()
                    ordered_image = OrderedImage(gallery=gallery, image=image, position=index)
                    ordered_image.save()
                post = PostWithSlideshow(title=title, slug=slugify(title),
                                            subtitle=subtitle, body=post_body,
                                            gallery=gallery)
                post.save()
            if post:
                # Saves the authors and tags of the post
                for index, author in enumerate(authors):
                    credit = OrderedCredit(credit=Credit.objects.get(id=author), 
                                            content_object=post, position=index)
                    credit.save()
                for index, tag in enumerate(tags):
                    tag = TaggedItem(tag=Tag.objects.get(id=tag), object=post)
                    tag.save()
                article = SubmittedArticle(submitted_by=request.user, object=post)
                article.save()
            return HttpResponseRedirect(reverse('submit_article_success'))
    else:
        form = ArticleSubmissionForm()
        image_forms = ImageFormset()
    return render_to_response('submit_article/add.html',
                            {'form': form,
                            'image_forms': image_forms,
                            'max_forms': settings.MAX_NUM_IMAGES},
                            context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def clear_cache(request):
    cache.clear()
    return HttpResponse(unicode(_('The cache has been cleared.')))


def print_post(request, slug):
    post = get_object_or_404(BasicPost, slug=slug)

    has_image = False
    if post.get_class_name() == 'PostWithImage':
        post = post.postwithimage
        has_image = True
    elif post.get_class_name() == 'PostWithSimpleImage':
        post = post.postwithsimpleimage
        has_image = True
        
    context = {'post':post,
               'has_image':has_image,}
    return render_to_response('post/post_print.html',
                              context,
                              RequestContext(request))
