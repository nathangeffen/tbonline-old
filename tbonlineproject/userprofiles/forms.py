from django import forms
from django.contrib.auth.models import User
from userprofiles.models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',
                  'date_of_birth',
                  'website',)
