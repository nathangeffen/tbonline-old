from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.contrib import messages

from notifications.models import CommentNotification, PostNotification, AlreadyNotifiedError


def notify(request, NotificationType, name,
           login_msg=_('You need to login to receive notifications.'),
           success_msg=_("You will receive emails alerting you to new posts."), 
           already_msg=_("You already receive notifications for new posts"),
           *args):
    '''Common method for processing different types of notification view. 

    '''

    if not request.user.is_authenticated:
        messages.warning(request, login_msg)    

    try:
        c = NotificationType()
        c.add_user(name, request.user, *args)
        messages.info(request, success_msg)
    except AlreadyNotifiedError:
        messages.warning(request, already_msg)
    except (ValueError, KeyError):
        messages.warning(request, _("An unexpected error has occurred in "
                                "the notification system"))
 
    try:
        return HttpResponseRedirect(request.GET['next'])
    except:
        raise Http404    
    

def notify_post(request, name='post'):
    '''Process notification request, typically after user submits form requesting to be
    notified of new comments on a post. 
    
    '''
    return notify(request, PostNotification, name)    

def notify_comment(request, name='comment'):
    '''Process notification request, typically after user submits form requesting to be
    notified of new comments on a post. 
    
    '''
 
    return notify(request, CommentNotification, name,
                  None,
                  _("You will receive emails notifying you of new comments on this post."),
                  _("You already receive emails notifying you of new comments on this post."), 
                  request.GET['app_label'], 
                  request.GET['model'], int(request.GET['pk']))   
    

def remove_notification(request, NotificationType, name, 
                        success_msg=_('You will no longer receive emails notifying you of new posts.'), 
                        already_msg=_('You do not get emailed notifications of new posts.'), 
                        *args):
    try:
        try:
            notification = NotificationType.objects.get(name=name)
        except:
            notification = NotificationType()

        notification.remove_user(request.GET['user'], *args)
        messages.info(request, success_msg)        
    except:
        messages.info(request, already_msg)

    try:        
        return HttpResponseRedirect(request.GET['next'])
    except:
        raise Http404    

def remove_post_notification(request, name='post'):
    return remove_notification(request, PostNotification, name)

def remove_comment_notification(request, name='comment'):
    return remove_notification(request, CommentNotification, name,
                                    _('You will no longer receive emails notifying you of new comments on this post.'),
                                    _('You do not receive emails notifying you of new comments on this post.'), 
                                    request.GET['app_label'],
                                    request.GET['model'],
                                    int(request.GET['pk']))
