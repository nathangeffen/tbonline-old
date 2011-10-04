import sys
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.sites.models import Site 
from django.template import Context, Template, TemplateSyntaxError, \
    TemplateDoesNotExist, loader
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.validators import email_re

from notifications.models import Notification, Recipient

def is_valid_email(email):
    return True if email_re.match(email) else False


class Command(BaseCommand):
    args = '<notification_name notification_name ...>'
    help = 'Processes notification for the specified Notifications'

    def execute_notifications(self, names):
        ''' Creates a dictionary called email_list in the following form:
        
        [{'notification': Notification,
        'user' : user,
        'site' : site,
        'objects' : [o1, o2, o3 ... on],
        
        ''' 
        if names:
            notifications = Notification.objects.active().filter(name__in=names).select_subclasses()
        else:
            notifications = Notification.objects.active().select_subclasses()
        
        self.email_list = {}
    
        total_emails_processed = 0
    
        for notification in notifications:
            execution_time = datetime.now()
            objects = notification.querydef()
            
            recipients = Recipient.objects.filter(notification__pk=notification.pk)
            
            context = {}
            context['notification'] = notification
            context['site'] = Site.objects.get_current()
            context.update(notification.get_context_data())
            
            for r in recipients:
                context['objects'] = []
                for i, o in enumerate(objects):
                
                    if notification.is_digest: 
                        context['objects'].append(o)
                    else:
                        context['objects'] = [o]
                                        

                context['user'] = r.user
                if is_valid_email(r.user.email) and context['objects']:
                    if notification.is_digest:
                        self.email_list[r.user.email+notification.name] = context.copy()
                    else:
                        self.email_list[r.user.email+notification.name+unicode(i)] = context.copy()
         
            self.send_mails()
            total_emails_processed += len(self.email_list)
            
            sys.stdout.write('Processed %d emails for notification: %s.\n' 
                            % (len(self.email_list), unicode(notification)))
                    
            if len(objects):
                notification.last_executed = execution_time
                notification.save()
                sys.stdout.write('Notification %s execution time %s written to database\n'
                                  % (unicode(notification), unicode(execution_time)))
            
        sys.stdout.write("Total emails processed: %d\n" % total_emails_processed)
        
        return total_emails_processed    

    def handle(self, *args, **options):
        
        if len(args):        
            self.execute_notifications(args)

    def send_mails(self):
        for key, context in self.email_list.iteritems():
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = context['user'].email
            notification = context['notification']
            
            if notification.subject_template:
                t = loader.get_template(notification.subject_template)
            else:
                t  = loader.get_template('notifications/notification_'+ 
                                        notification.name.lower() +'_subject.txt')
            
            c = Context(context)
            subject = t.render(c)
                
            if notification.body_template:
                t = loader.get_template(notification.body_template)
            else:  
                t = loader.get_template('notifications/notification_'+ 
                                        notification.name.lower() +'_email.txt')

            c = Context(context)
            body = t.render(c)
            
            send_mail(subject, body, from_email, [to_email], fail_silently=False)
                
            