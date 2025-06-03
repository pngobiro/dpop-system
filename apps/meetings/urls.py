# apps/meetings/urls.py
from django.urls import path
from apps.meetings.views import (
    calendar_view, director_dashboard, meeting_list,
    dashboard, meeting_create, meeting_detail,
    meeting_update, meeting_delete, add_quick_meeting,
    add_meeting_attachment_comment, add_meeting_participant,
    meeting_action
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
    path('attachment/<int:attachment_id>/comment/', add_meeting_attachment_comment, name='add_meeting_attachment_comment'),
    path('<int:pk>/edit/', meeting_update, name='meeting_update'),
    path('<int:pk>/delete/', meeting_delete, name='meeting_delete'),
    path('<int:pk>/add-participant/', add_meeting_participant, name='add_meeting_participant'),
    path('<int:pk>/action/<str:action>/', meeting_action, name='meeting_action'),
]