from django.contrib import admin

from models import Feed, Entry

class FeedAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'title', 'url', 'number_of_items', 'position', 'keep_old_items', 'active',)
    list_editable = ('title', 'url', 'number_of_items', 'position','keep_old_items', 'active',)
    prepopulated_fields = {"slug": ("title",)}
    
class EntryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'feed', 'title', 'date_added', )
    list_filter = ('feed',)
    

admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
