'''Admin interface registers Image model with admin.site. 
'''
from django.contrib import admin

from notifications.models import Notification, CommentNotification, Recipient

admin.site.register(Notification)
admin.site.register(CommentNotification)
admin.site.register(Recipient)
