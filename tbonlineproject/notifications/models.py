from datetime import datetime
import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User 
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.db import IntegrityError

from model_utils.managers import InheritanceManager

from post.models import BasicPost

class AlreadyNotifiedError(Exception):
    """Exception raised when trying to add an existing user to a notification 

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg

    def __unicode__(self):
        return self.msg

class NotificationManager(InheritanceManager):
    def active(self):
        return super(NotificationManager, self).get_query_set().filter(active=True)        
 

class Notification(models.Model):    
    name = models.CharField(max_length=200)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_digest = models.BooleanField(default=True)
    subject_template = models.CharField(max_length=200, blank=True)
    body_template = models.CharField(max_length=200, blank=True)    
    last_pk = models.PositiveIntegerField(blank=True, null=True) 
    last_executed = models.DateTimeField()
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    objects = NotificationManager()

    def add_user(self, name, user, NotificationClass=None):
        # Get notification. If it does not exist add it.
        
        if not NotificationClass:
            NotificationClass = Notification
        
        try:
            self = NotificationClass.objects.get(name=name)
        
            # Make Notification it active if it is inactive
            if self.active == False:
                self.active = True
                self.save()
        
        except PostNotification.DoesNotExist:
            self = NotificationClass.objects.create(name=name,
                                        last_executed=datetime.now())
        finally:
            # Add Recipient user.
            try:  
                Recipient.objects.create(notification=self, user=user)
            except IntegrityError:
                raise AlreadyNotifiedError(ugettext('%s already gets notified of new comments on this item.' % user))

        return self

    def remove_user(self, user, *args):
        Recipient.objects.filter(notification=self, user__username=user).delete()

    def get_context_data(self):
        return {}

    def querydef(self):
        return []

    def is_notified(self, name, user):
        try:
            Recipient.objects.get(notification__name=name, user=user)
            return True
        except Recipient.DoesNotExist:
            return False
        
    
    def __unicode__(self):
        return self.__class__.__name__ + ugettext(' ') + unicode(self.last_executed)
    
    class Meta:
        ordering = ('last_modified',)


class Recipient(models.Model):
    notification = models.ForeignKey(Notification)
    user = models.ForeignKey(User, null=True, blank=True)
        
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)    
    
    def __unicode__(self):
        return unicode(self.notification) + ugettext(' - ') + self.user.username

    class Meta:
        ordering = ('notification','user',)
        unique_together = ('notification', 'user',)
                

class PostNotification(Notification):

    def add_user(self, name, user, *args):
        return super(PostNotification, self).add_user(name, user, PostNotification)
    
    def querydef(self):
        return BasicPost.objects.published().\
            filter(date_published__gte=self.last_executed).select_subclasses()

class CommentNotification(Notification):
    linked_content_type = models.ForeignKey(ContentType)
    linked_object_id = models.PositiveIntegerField()
    linked_content_object = generic.GenericForeignKey('linked_content_type', 
                                                      'linked_object_id')

    def add_user(self, name, user, app_label, model, pk):
        '''Create a notification if it doesn't exist and 
        add the recipient user.  
        
        '''
        
        if not name:
            name = 'comment'
            
        # Get notification. If it does not exist add it.
                
        ct = ContentType.objects.get(app_label=app_label, model=model)

        try:
            self = CommentNotification.objects.get(name=name,
                                linked_content_type=ct,
                                linked_object_id=int(pk))

            # Make Notification it active if it is inactive
            if self.active == False:
                self.active = True
                self.save()
            
        except CommentNotification.DoesNotExist:
            # Add the notification since it does not exist

            self = CommentNotification.objects.create(name='comment',
                                        linked_content_type=ct,
                                        linked_object_id=pk,
                                        last_executed=datetime.now())                
        finally:
            # Add Recipient user.
            try:  
                Recipient.objects.create(notification=self, user=user)
            except IntegrityError:
                raise AlreadyNotifiedError(ugettext('%s already gets notified of new comments on this item.' % user))

        return self

    def remove_user(self, user, app_label, model, pk):
        ct = ContentType.objects.get(app_label=app_label, model=model)
        try:
            self = CommentNotification.objects.get(name='comment',
                                linked_content_type=ct,
                                linked_object_id=pk)
        except CommentNotification.DoesNotExist:
            pass
        
        Recipient.objects.filter(notification=self, user__username=user).delete()
            
    def querydef(self):
        return Comment.objects.filter(content_type=self.linked_content_type, 
                               object_pk=self.linked_object_id, 
                               submit_date__gt=self.last_executed,
                               is_public=True,
                               is_removed=False)

                
    def get_context_data(self):
        context = {}
        context['url'] = self.linked_content_object.get_absolute_url()
        context['description'] = unicode(self.linked_content_object)
        return context

    def is_notified(self, name, user, obj):
        try:
            ct = ContentType.objects.get_for_model(obj)
            self = CommentNotification.objects.get(name=name,
                                linked_content_type=ct,
                                linked_object_id=obj.pk)
            Recipient.objects.get(notification__pk=self.pk, user=user)
            return True
        except (CommentNotification.DoesNotExist, Recipient.DoesNotExist):
            return False
    
    class Meta:
        unique_together = ('linked_content_type', 'linked_object_id')
    