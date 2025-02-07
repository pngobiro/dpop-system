# apps/mail/urls.py
from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('physical/', views.mail_dashboard, name='mail_dashboard'),
    path('physical/register/', views.register_mail, name='register_mail'),
    path('physical/<int:pk>/', views.mail_detail, name='mail_detail'),  # Added
    path('physical/<int:pk>/movement/', views.record_mail_movement, name='record_movement'),
    path('physical/movement-report/', views.mail_movement_report, name='mail_movement_report'),
    path('physical/<int:pk>/dispatch/', views.dispatch_mail, name='dispatch_mail'),
]