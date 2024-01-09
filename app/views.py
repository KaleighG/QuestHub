from django.shortcuts import render, redirect, get_object_or_404
from app.form import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')

@login_required
def messages(request):
    return render(request, "message.html")

@login_required
def profile(request):
    return render(request, "profile.html")

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        return render(request, "register.html", {"form":CreateUserForm()})
    return render(request, "register.html", {"form":form})

@login_required
def usersettings(request):
    return render(request, "usersettings.html")