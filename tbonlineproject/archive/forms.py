import re

from django import forms
from tagging.models import Tag

from django.utils.translation import ugettext as _

class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag

    def clean_name(self):
        value = self.cleaned_data['name']
        m=re.match("([\w| |_|-]+)$",value)
        
        if not m:
            raise forms.ValidationError(_('Tags can only contain alphanumeric '
                                          'characters, spaces, dashes and underscores.'))
        
        return value
