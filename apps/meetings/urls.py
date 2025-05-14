# apps/meetings/urls.py
from django.urls import path
from .views import calendar_view, dashboard, director_dashboard, meeting_list
from .views.crud import (
    meeting_create, meeting_detail, meeting_update,
    meeting_delete, add_quick_meeting
)

app_name = 'meetings'

urlpatterns = [
    path('calendar/', calendar_view, name='calendar'),
    path('', dashboard, name='dashboard'),
    path('director/', director_dashboard, name='director_dashboard'),
    path('list/', meeting_list, name='meeting_list'),
    path('create/', meeting_create, name='meeting_create'),
    path('quick-add/', add_quick_meeting, name='add_quick_meeting'),
    path('<int:pk>/', meeting_detail, name='meeting_detail'),
    path('<int:pk>/edit/', meeting_update, name='meeting_update'),
    path('<int:pk>/delete/', meeting_delete, name='meeting_delete'),
]