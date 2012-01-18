from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('profiles.views',
    url(r'^update/$', 'update_profile', name='update_profile'),

)
