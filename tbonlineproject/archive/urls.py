from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

from archive.models import Catalogue, Document

urlpatterns = patterns('archive.views',   

    url(r'^$', 
        ListView.as_view(
                    context_object_name="catalogues",
                    queryset=Catalogue.objects.all(),
                    template_name='archive/catalogues.html'), name='catalogue-list'),

    url(r'^(?P<pk>\d+)$', 
        DetailView.as_view(
                    context_object_name="catalogue",
                    queryset=Catalogue.objects.all(),
                    template_name='archive/catalogue.html'), name='catalogue-detail'),

    
    url(r'^documents/$', 
        ListView.as_view(
                    context_object_name="documents",
                    queryset=Document.objects.all(),
                    template_name='archive/documents.html'), name='document-list'),

    
    url(r'^document/(?P<pk>\d+)/$', 
        DetailView.as_view(
                    context_object_name="document",
                    queryset=Document.objects.all(),
                    template_name='archive/document.html'), name='document-detail'),
)
