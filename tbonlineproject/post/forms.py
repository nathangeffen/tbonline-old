from django import forms
from django.utils.translation import ugettext as _

from contact_form.forms import ContactForm 
from stopspam.forms import HoneyPotForm
from stopspam.forms.fields import HoneypotField

class EnhancedContactForm(ContactForm):
    error_css_class = 'error'
    required_css_class = 'required'

    # This field will not be displayed to web users.
    # Hopefully spam bots will fill it in.
    accept_terms = HoneypotField() 
                                    
    subject = forms.CharField(max_length=100,
                           label=_('Subject'))
    
    def __init__(self, *args, **kwargs):
        ContactForm.__init__(self, *args, **kwargs)
        self.fields.keyOrder = ['name', 'email', 'subject', 'accept_terms', 'body']
