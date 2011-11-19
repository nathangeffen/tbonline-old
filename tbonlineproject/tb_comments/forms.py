from django import forms
from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment

from tb_comments.fields import ReCaptchaField

class CommentFormWithRecaptcha(CommentForm):
    recaptcha = ReCaptchaField()

    def get_comment_model(self):
        return Comment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentForm, self).get_comment_create_data()
        return data
