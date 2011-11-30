from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _

from contact_form.forms import ContactForm 
from stopspam.forms.fields import HoneypotField

from credit.models import Credit
from enhancedtext.fields import EnhancedTextWidget
from gallery.models import Image
from post.models import BasicPost
from tagging.models import Tag
from CommentRecaptcha.fields import ReCaptchaField

class EnhancedContactForm(ContactForm):
    error_css_class = 'error'
    required_css_class = 'required'

    # This field will not be displayed to web users.
    # Hopefully spam bots will fill it in.
    accept_terms = HoneypotField() 
    subject = forms.CharField(max_length=100,
                           label=_('Subject'))
                                    
    
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")

        if request.user.is_authenticated():
            kwargs['initial'] = {'name' : request.user.get_full_name() if request.user.get_full_name() != u''  else request.user.username,
                                 'email' : request.user.email}
                                 
            
        super(EnhancedContactForm, self).__init__(data=data, 
                                                  files=files, 
                                                  request=request, 
                                                  *args, 
                                                  **kwargs)

        if not request.user.is_authenticated():
            self.fields['recaptcha'] = ReCaptchaField()
            self.fields.keyOrder = ['name', 'email', 'subject', 'accept_terms', 'body', 'recaptcha']
        else:
            self.fields.keyOrder = ['name', 'email', 'subject', 'accept_terms', 'body']
            
class ArticleSubmissionForm(forms.Form):
    EDITOR_CHOICES = (
        ('\W', _('HTML editor')),
        ('\M', _('Markdown')), 
    )
    
    error_css_class = 'error'
    required_css_class = 'required'

    title = forms.CharField(max_length=200, label=_('Title'))
    subtitle = forms.CharField(max_length=200, label=_('Subtitle'), required=False)
    body = forms.CharField(label=_('Body'), widget=forms.Textarea)
    editor = forms.ChoiceField(label=_('Editor'), choices=EDITOR_CHOICES, required=False)
    authors = forms.ModelMultipleChoiceField(label=_('Authors'), help_text=_("(You may select multiple authors or leave it blank)"),
                                            queryset=Credit.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(label=_('Tags'), help_text=_("(You may select multiple tags or leave it blank)"),
                                            queryset=Tag.objects.all().order_by('name'), required=False)
