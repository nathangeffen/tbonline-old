from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User 
from django.contrib.comments.models import Comment

class Notification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    template = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    last_pk = models.PositiveIntegerField(blank=True, null=True) 
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def get_querydef(self):
        pass

    def __unicode__(self):
        return self.name + _(' ') + unicode(self.last_executed)
    
    class Meta:
        abstract = True
        ordering = ('last_modified',)

class Recipient(models.Model):
    notification = models.ForeignKey(Notification)
    user = models.ForeignKey(User, null=True, blank=True)    
    email_override = models.EmailField(blank=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)    
    
    def __unicode__(self):
        return unicode(self.notification) + _(' - ') + self.user.username

    class Meta:
        ordering = ('notification','user',)
        unique_together = ('notification', 'user',)

def execute_notifications():
    notifications = Notification.objects.filter(active=True)
    
    for notification in notifications:
        objects = notification.querydef()
        recipients = Recipient.objects.filter(notification__pk=notification.pk)
        for o in objects: 
            for r in recipients:
                print r.username.email, unicode(o)
    
        notification.last_pk = objects 
                
class CommentNotification(Notification):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def get_querydef(self):
        Comment.objects.filter(content_type=self.content_type, 
                               object_id=self.object_id, pk__gt=self.last_pk)