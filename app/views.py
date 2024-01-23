from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from app.form import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from app.models import *

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})


@login_required
def messages(request):
    return render(request, "message.html")


def profile(request):
    # Get the profile of the currently logged-in user
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, "profile.html", {"user_profile": user_profile})


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
    form = PasswordChangeForm()
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
