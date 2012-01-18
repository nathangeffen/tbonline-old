from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars',
                               null=True,
                               blank=True,)
    date_of_birth = models.DateField(null=True,blank=True)
    website = models.URLField(null=True,blank=True)
