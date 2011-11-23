from django import forms

from tb_comments.fields import ReCaptchaField

class RecaptchaForm(forms.Form):
    recaptcha = ReCaptchaField()
