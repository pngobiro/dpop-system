# apps/permissions/urls.py
from django.urls import path
from . import views

app_name = 'apps.permissions'

urlpatterns = [
    path('manage/', views.manage_permissions, name='manage_permissions'),
    path('assign-departments/', views.assign_departments, name='assign_departments'),  # New URL
]