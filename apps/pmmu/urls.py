# apps/pmmu/urls.py
from django.urls import path
from . import views

app_name = 'apps.pmmu'

urlpatterns = [
    path('dashboard/', views.pmmu_dashboard, name='pmmu_dashboard'),
    path('pmmus/<int:pmmu_pk>/indicators/', views.pmmu_item_list, name='pmmu_item_list'),
    path('indicators/<int:pk>/', views.indicator_detail, name='indicator_detail'), 
    path('pmmu_item_detail/<int:pk>/', views.pmmu_item_detail, name='pmmu_item_detail'),
    path('indicator_list/<int:pmmu_pk>/', views.indicator_list, name='indicator_list'),
]