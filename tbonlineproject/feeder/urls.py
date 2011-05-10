from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from models import Feed

urlpatterns = patterns('feeder.views',
    url(r'^$', ListView.as_view(
                    context_object_name='feeds',
                    queryset=Feed.objects.filter(active=True),
                    template_name='feeder/listfeeders.html'),name='listfeeders'),
    
    url(r'^(?P<slug>[a-zA-Z0-9-_]+)/$', 
        DetailView.as_view(
                    context_object_name="feed",
                    queryset=Feed.objects.filter(active=True),                    
                    template_name='feeder/detailfeeder.html'), name='detailfeeder'),    
)
