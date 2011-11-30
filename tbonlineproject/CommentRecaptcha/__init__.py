from django.core.urlresolvers import reverse

def get_form_target():
    return reverse('comment-verify-comment')
