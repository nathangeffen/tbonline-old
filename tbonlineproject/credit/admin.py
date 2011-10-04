'''Admin interface for credit app exposes Inline for ordered credits and
registers Credit model with admin interface. 

'''

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.forms.widgets import HiddenInput
from django.db.models import PositiveIntegerField
from django.utils.translation import ugettext as _

from models import Credit, OrderedCredit

class OrderedCreditInline(generic.GenericTabularInline):
    verbose_name = _('author or source')
    verbose_name_plural = _('authors or sources')    
    classes = ('collapse open',)    
    model = OrderedCredit
    raw_id_fields = ('credit',)
    related_lookup_fields = {
        'fk': ['credit'],
    }    

    extra = 0
    
    formfield_overrides = {
        PositiveIntegerField: {'widget': HiddenInput},
    }    
    
    sortable_field_name = 'position'

class CreditAdmin(admin.ModelAdmin):
    search_fields = ('first_names','last_name')
    list_display = ('id', 'first_names', 'last_name', 'is_person', 'url')
    list_editable = ('first_names', 'last_name', 'is_person', 'url')
    list_filter = ('is_person',)    

class OrderedCreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'content_object', 'position', 'credit')

admin.site.register(Credit, CreditAdmin)
admin.site.register(OrderedCredit, OrderedCreditAdmin)