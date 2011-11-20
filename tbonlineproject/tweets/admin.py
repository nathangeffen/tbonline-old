from django.contrib import admin
from tweets.models import TwitterUsername, Hashtag

admin.site.register(TwitterUsername)
admin.site.register(Hashtag)
