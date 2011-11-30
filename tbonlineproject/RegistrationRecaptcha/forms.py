from registration.forms import RegistrationForm

from CommentRecaptcha.fields import ReCaptchaField

class RegistrationFormRecaptcha(RegistrationForm):
    recaptcha = ReCaptchaField()
