from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from app.form import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from app.models import *
from django.db.models import Q
import openai

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


def delete_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient)
        | Q(sender=recipient, recipient=request.user)
    )
    for message in messages:
        message.delete()
    return redirect('message')


def chatgpt_image_creator(request):
    if request.method == 'POST':
        form = ChatGPTForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']

            # Call OpenAI API to generate image using input_text
            # Remember to replace 'your-api-key' with your actual OpenAI API key
            openai.api_key = 'your-api-key'
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=input_text,
                max_tokens=150
            )

            generated_image = response['choices'][0]['text']
            return render(request, 'yourapp/result.html', {'generated_image': generated_image})

    else:
        form = ChatGPTForm()

    return render(request, 'yourapp/chatgpt_form.html', {'form': form})
