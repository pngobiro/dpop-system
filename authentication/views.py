# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, CustomPasswordChangeForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # Import Django's built-in User model
from django.contrib.auth.forms import UserCreationForm # Import UserCreationForm
from django.urls import reverse_lazy # Import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # Import generic views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Import mixins for access control
from .models import CustomUser
from apps.organization.models import Department
from django import forms
from django.db import models
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

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

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'pj_number', 'phone', 'mobile', 'departments', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']

class CustomUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'authentication/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(username__icontains=q) |
                models.Q(email__icontains=q) |
                models.Q(first_name__icontains=q) |
                models.Q(last_name__icontains=q) |
                models.Q(phone__icontains=q) |
                models.Q(mobile__icontains=q) |
                models.Q(pj_number__icontains=q)
            )
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(departments__id=department)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['department'] = self.request.GET.get('department', '')
        context['departments'] = Department.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_staff

class CustomUserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'authentication/user_form.html'
    success_url = reverse_lazy('authentication:user_list')

    def form_valid(self, form):
        # Generate a random password
        password = get_random_string(length=10)
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        form.save_m2m()
        # Send welcome email
        login_url = self.request.build_absolute_uri(reverse_lazy('authentication:login'))
        subject = 'Welcome to the Platform'
        message = render_to_string('authentication/welcome_email.txt', {
            'user': user,
            'password': password,
            'login_url': login_url,
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        messages.success(self.request, f"User '{user.username}' created and welcome email sent.")
        return super().form_valid(form)
    def test_func(self):
        return self.request.user.is_staff

class CustomUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'authentication/user_form.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('authentication:user_list')
    def test_func(self):
        return self.request.user.is_staff

class CustomUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'authentication/user_confirm_delete.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('authentication:user_list')
    def test_func(self):
        return self.request.user.is_staff

@login_required
def regenerate_password(request, pk):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('authentication:user_list'))
    user = CustomUser.objects.get(pk=pk)
    new_password = get_random_string(length=10)
    user.set_password(new_password)
    user.save()
    messages.success(request, f"Password for user '{user.username}' has been reset. New password: {new_password}")
    return redirect('authentication:user_update', pk=pk)

@login_required
def send_welcome_email_view(request, pk):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('authentication:user_list'))
    user = CustomUser.objects.get(pk=pk)
    # Generate a new random password and set it (optional, or use existing password)
    password = get_random_string(length=10)
    user.set_password(password)
    user.save()
    # Send welcome email
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.conf import settings
    login_url = request.build_absolute_uri(reverse_lazy('authentication:login'))
    subject = 'Welcome to the Platform'
    message = render_to_string('authentication/welcome_email.txt', {
        'user': user,
        'password': password,
        'login_url': login_url,
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    messages.success(request, f"Welcome email sent to '{user.username}' with a new password.")
    return redirect('authentication:user_update', pk=pk)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('authentication:settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'authentication/change_password.html', {'form': form})




