from django.urls import path
from . import views

app_name = 'apps.home'


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments/<int:department_id>/modules/', views.department_modules, name='department_modules'), # New URL for department modules
]