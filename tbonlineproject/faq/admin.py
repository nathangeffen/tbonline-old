from django.contrib import admin
from django.forms.widgets import HiddenInput
from django.db.models import PositiveIntegerField

from faq.models import QuestionAndAnswer, QuestionCategory

class QuestionAndAnswerInline(admin.StackedInline):
    model = QuestionAndAnswer
    classes = ('collapse open')
    sortable_field_name = 'position'
    formfield_overrides = {
        PositiveIntegerField: {'widget': HiddenInput},
    }    
    extra = 0
    
class QuestionAndAnswerAdmin(admin.ModelAdmin):
    search_fields = ('category__name', 'question', 'answer',)
    list_display = ('id', 'category', 'question', 'answer', 'position',)
    list_editable = ('category', 'question', 'answer', 'position',)
    list_filter = ('category',)

class QuestionCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('id', 'name',)
    list_editable = ('name',)
    inlines = [QuestionAndAnswerInline,]

admin.site.register(QuestionAndAnswer, QuestionAndAnswerAdmin)
admin.site.register(QuestionCategory, QuestionCategoryAdmin)
