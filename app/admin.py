from django.contrib import admin
from app.models import UserProfile

# Register your models here.

from app.models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "profile_pic", "bio", "color_blind_mode")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "message", "date")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("creator", "image", "caption", "date")
