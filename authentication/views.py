# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required



#dashboard
def dashboard(request):
    return render(request, "accounts/dashboard.html")


#profile
def view_profile(request):
    return render(request, "accounts/profile.html")

#edit_profile
def edit_profile(request):
    return render(request, "accounts/edit_profile.html")


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/tasks/my_dashboard/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

class CustomLogoutView(LogoutView):
    next_page = '/login/'

@login_required
def profile_view(request):
    """
    View for displaying the current user's profile.
    """
    return render(request, 'authentication/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    """
    View for displaying and potentially updating user settings.
    """
    return render(request, 'authentication/settings.html', {'user': request.user})




