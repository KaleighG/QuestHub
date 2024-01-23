from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from app.form import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from app.models import *
from django.db.models import Q

# Create your views here.


def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        searched = request.POST.get("searched")
        if searched:
            posts = Post.objects.filter(caption__icontains=searched)

    return render(request, "home.html", {"posts": posts})


@login_required
def messages(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by("-date")
    latest_messages = {}
    for message in messages:
        other_user = (
            message.recipient if message.sender == request.user else message.sender
        )
        if other_user not in latest_messages:
            latest_messages[other_user] = message
    return render(request, "message.html", {"messages": latest_messages})


def profile(request, user_id):
    friends = Friend.objects.filter(Q(user_profile=request.user.profile)|Q(friend_profile=request.user.profile))
    requests = Friend_Request.objects.filter(recipient=request.user, status='pending')
    requests_ids = [request.sender for request in requests]
    profiles = UserProfile.objects.filter(user__in=requests_ids)
    search_people = UserProfile.objects.all()
    user_profile = UserProfile.objects.get(user__id=user_id)
    return render(request, "profile.html", {"user_profile": user_profile, "friends":friends, "profiles": profiles, "search_people":search_people})


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST.get("username"))
            UserProfile.objects.create(user=user, role="User")
            return redirect("login")
    else:
        return render(request, "register.html", {"form": CreateUserForm()})
    return render(request, "register.html", {"form": form})


@login_required
def usersettings(request):
    return render(request, "usersettings.html")


def changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        return redirect("usersettings")


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            return redirect("profile")
    else:
        form = CreatePostForm()
    return render(request, "create_post.html", {"form": form})


@login_required
def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient)
        | Q(sender=recipient, recipient=request.user)
    ).order_by("date")
    if request.method == "POST":
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            message=request.POST.get("message"),
        )
        return redirect("send_message", recipient_id=recipient_id)
    return render(
        request,
        "send_message.html",
        {"messages": messages, "recipientid": recipient_id},
    )


def delete_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient)
        | Q(sender=recipient, recipient=request.user)
    )
    for message in messages:
        message.delete()
    return redirect('message')

def send_friend_request(request, user_id):
    recipient = UserProfile.objects.get(user__id=user_id)
    request.user.profile.send_friend_request(recipient.user)
    return redirect("home")


def accept_friend_request(request, user_id):
    friend_request = Friend_Request.objects.get(sender=user_id, recipient=request.user)
    friend_request.recipient.profile.accept_friend_request(friend_request)
    return redirect("friends")


def decline_friend_request(request, user_id):
    friend_request = Friend_Request.objects.get(sender=user_id, recipient=request.user)
    request.user.profile.decline_friend_request(friend_request)
    return redirect("friends")

def remove_friend(request, friend_id):
    friendObj = Friend.objects.get(id=friend_id)
    friendObj.delete()
    return redirect("friends")

