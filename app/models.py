from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="media", blank=True, null=True)
    bio = models.CharField(max_length=250, null=True, blank=True)
    color_blind_mode = models.CharField(max_length=20, default="default")
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    def send_friend_request(self, to_user):
        Friend_Request.objects.create(
            sender=self.user, recipient=to_user, status="pending"
        )

    def accept_friend_request(self, friend_request):
        friend_request.status = "accepted"
        friend_request.save()
        self.friends.add(friend_request.sender.profile)
        Friend.objects.create(
            user_profile=self, friend_profile=friend_request.sender.profile
        )

    def decline_friend_request(self, friend_request):
        friend_request.status = "declined"
        friend_request.save()

    def remove_friend(self, other_user):
        self.friends.remove(other_user)

    def are_friends(self, user_profile):
        return self.friends.filter(id=user_profile.id).exists()
    

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
    def __str__(self):
        return f"{self.message}"



class Friend(models.Model):
    user_profile = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, related_name="user_profile"
    )
    friend_profile = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, related_name="friend_profile"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user_profile.user.username} - {self.friend_profile.user.username}"
        )


class Friend_Request(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_requests"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests"
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("declined", "Declined"),
            ("cancelled", "Cancelled"),
        ],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

