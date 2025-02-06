# authentication/urls.py
from django.urls import path
from .views import login_view, register_user, view_profile, edit_profile
from django.contrib.auth.views import LogoutView
from .views import CustomLogoutView
from django.urls import include

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
