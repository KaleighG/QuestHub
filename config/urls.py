"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", home, name="home"),
    path("profile/", profile, name="profile"),
    path("messages/", messages, name="message"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("usersettings/", usersettings, name="usersettings"),
    path("changepassword/", changepassword, name="changepassword"),
    path("create_post", create_post, name="create_post"),
    path("send_message/<int:recipient_id>/", send_message, name="send_message"),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
