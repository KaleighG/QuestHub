from django.contrib import admin
from app.models import UserProfile
# Register your models here.

from app.models import UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","role","profile_picture","friends","bio")