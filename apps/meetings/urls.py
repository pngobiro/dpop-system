# apps/meetings/urls.py
from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),  # Add this line
    path('', views.dashboard, name='dashboard'),
    path('director/', views.director_dashboard, name='director_dashboard'),
    path('list/', views.meeting_list, name='meeting_list'),
    path('create/', views.meeting_create, name='meeting_create'),
    path('<int:pk>/', views.meeting_detail, name='meeting_detail'),
    path('<int:pk>/edit/', views.meeting_update, name='meeting_update'),
    path('<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),
]