import re
from django import template
from notifications.models import Notification, CommentNotification

register = template.Library()

class NotificationsChecker(template.Node):
    def __init__(self, notification_name, var_name):
        self.notification_name = notification_name
        self.var_name = var_name

    def render(self, context):
        try:
            n = Notification()
            context[self.var_name] =  n.is_notified(self.notification_name,
                                                context['user'])
        except:
            pass

        return ""

def do_is_notified(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        template_tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    
    m = re.search(r'(\"\w+\") as (\w+)', arg)
        
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % template_tag_name)
    
    notification_name, var_name = m.groups()
    return NotificationsChecker(notification_name[1:-1], var_name)

register.tag('is_notified', do_is_notified)


class CommentNotificationsChecker(template.Node):
    def __init__(self, notification_name, obj, var_name):
        self.notification_name = notification_name
        self.obj = template.Variable(obj)
        self.var_name = var_name

    def render(self, context):
        try:
            n = CommentNotification()
            context[self.var_name] =  n.is_notified(self.notification_name,
                                                    context['user'],
                                                    self.obj.resolve(context))
        except:
            pass

        return ""

def do_is_comment_notified(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        template_tag_name, notification_name, obj, _as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % template_tag_name)

    return CommentNotificationsChecker(notification_name[1:-1], obj,var_name)

register.tag('is_comment_notified', do_is_comment_notified)
