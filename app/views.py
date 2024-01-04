from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, "profile.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def usersettings(request):
    return render(request, "usersettings.html")