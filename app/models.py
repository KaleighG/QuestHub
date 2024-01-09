
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='media', blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=True)
    bio = models.CharField(max_length=250, null=True, blank=True)