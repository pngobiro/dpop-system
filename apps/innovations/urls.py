# apps/innovations/urls.py
from django.urls import path
from . import views

app_name = 'apps.innovations'

urlpatterns = [
    path('submit/', views.submit_innovation, name='submit_innovation'),
    path('list/', views.innovation_list, name='innovation_list'),
    path('approve/<int:pk>/', views.approve_innovation, name='approve_innovation'),
    path('reject/<int:pk>/', views.reject_innovation, name='reject_innovation'),
    path('detail/<int:pk>/', views.innovation_detail, name='innovation_detail'),
    path('edit/<int:pk>/', views.edit_innovation, name='edit_innovation'),
    path('delete/<int:pk>/', views.delete_innovation, name='delete_innovation'),
    path('download/<int:attachment_id>/', views.download_attachment, name='download_attachment'),
    path('', views.dashboard, name='dashboard'),  # Add the dashboard URL
]