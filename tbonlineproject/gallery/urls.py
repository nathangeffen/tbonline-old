from django.conf.urls.defaults import *
from django.views.generic import DetailView
from models import Image

urlpatterns = patterns('gallery.views',   
    url(r'^image/(?P<pk>\d+)/$', 
        DetailView.as_view(
                    context_object_name="image",
                    queryset=Image.objects.all(),
                    template_name='gallery/image.html'), name='image_view'),
    
)
