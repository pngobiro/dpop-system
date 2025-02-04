# apps/budget/urls.py
from django.urls import path
from . import views

app_name = 'apps.budget'

urlpatterns = [
    path('workplan/', views.workplan_summary, name='workplan_summary'),
    path('initiatives/', views.transformative_initiatives, name='transformative_initiatives'),
    path('indicators/', views.performance_indicators, name='performance_indicators'),
]
