from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="media", blank=True, null=True)
    bio = models.CharField(max_length=250, null=True, blank=True)
    color_blind_mode = models.CharField(max_length=20, default="default")


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        max_length=350, upload_to="images/", null=True, blank=True
    )
    caption = models.TextField(max_length=350)
    date = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    message = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
