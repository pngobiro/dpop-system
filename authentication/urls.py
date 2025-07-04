# authentication/urls.py
from django.urls import path
from .views import (
    login_view,
    register_user,
    CustomLogoutView,
    profile_view,
    settings_view,
    edit_profile,
    CustomUserListView,
    CustomUserCreateView,
    CustomUserUpdateView,
    CustomUserDeleteView,
    regenerate_password,
    send_welcome_email_view,
    change_password,
    # Password reset views
    password_reset_request,
    password_reset_confirm,
    password_reset_complete,
)

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Password Reset URLs
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-complete/', password_reset_complete, name='password_reset_complete'),
    
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('settings/', settings_view, name='settings'),
    path('settings/change_password/', change_password, name='change_password'),
    path('users/', CustomUserListView.as_view(), name='user_list'),
    path('users/create/', CustomUserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', CustomUserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', CustomUserDeleteView.as_view(), name='user_delete'),
    path('users/<int:pk>/regenerate_password/', regenerate_password, name='user_regenerate_password'),
    path('users/<int:pk>/send_welcome_email/', send_welcome_email_view, name='user_send_welcome_email'),
]
