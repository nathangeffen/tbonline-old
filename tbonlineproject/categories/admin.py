from django.contrib import admin
from categories.models import Category

from enhancedtext.admin import enhancedtextcss, enhancedtextjs

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', )
    list_editable = ('name',)
    
    class Media:
        css = enhancedtextcss 
        js = enhancedtextjs

admin.site.register(Category, CategoryAdmin)
