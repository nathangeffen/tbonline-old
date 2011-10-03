from django.conf.urls.defaults import *

urlpatterns = patterns('notifications.views',
    url(r'notify_comment/$', 'notify_comment', name='notify_comment'),
    
    url(r'notify_post/$', 'notify_post', name='notify_post'),
        
    url(r'remove_post_notification/$', 'remove_post_notification', 
        name='remove_post_notification'),
                       
    url(r'remove_comment_notification/$', 'remove_comment_notification', 
        name='remove_comment_notification'),
)
