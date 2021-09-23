from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("delete/", views.delete, name="delete"),
]
