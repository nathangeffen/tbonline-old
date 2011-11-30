from django import forms

from CommentRecaptcha.fields import ReCaptchaField

class RecaptchaForm(forms.Form):
    recaptcha = ReCaptchaField()
