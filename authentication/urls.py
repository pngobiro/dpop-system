# authentication/urls.py
from django.urls import path
from .views import (
    login_view,
    register_user,
    CustomLogoutView,
    profile_view,
    settings_view,
    edit_profile,
)

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('settings/', settings_view, name='settings'),
]
