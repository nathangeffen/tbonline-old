# Create your views here.

from django.views.generic import ListView, DateDetailView, DetailView, RedirectView
from post import app_settings as settings

from tagging.models import TaggedItem, Tag

class ItemsByTagView(ListView):
    context_object_name='items'
    paginate_by=settings.POSTS_PER_PAGE
    template_name='tagviews/tag_list_items.html'
    
    def get_queryset(self):
        try:
            tag = Tag.objects.get(name=self.kwargs["tag"])
            taggeditems = TaggedItem.objects.filter(tag=tag)
            return taggeditems
        except Tag.DoesNotExist:
            return []
        
    
    def get_context_data(self, **kwargs):
        context = super(ItemsByTagView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
