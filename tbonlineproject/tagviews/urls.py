from django.conf.urls.defaults import *

from tagviews.views import ItemsByTagView

urlpatterns = patterns('tagviews.views',   

    url(r'^(?P<tag>[\"\w\" \-]+)/$', ItemsByTagView.as_view(), name='tag_view'),

)
