from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'apps.home'


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments/<int:department_id>/modules/', views.department_modules, name='department_modules'), # New URL for department modules
    path('settings.html', TemplateView.as_view(template_name='home/settings.html'), name='settings_html'),
]