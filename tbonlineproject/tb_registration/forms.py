from registration.forms import RegistrationForm

from tb_comments.fields import ReCaptchaField

class RegistrationFormRecaptcha(RegistrationForm):
    recaptcha = ReCaptchaField()
