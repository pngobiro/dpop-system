# apps/pmmu/urls.py
from django.urls import path
from . import views

app_name = 'apps.pmmu'

urlpatterns = [
    path('dashboard/', views.pmmu_dashboard, name='pmmu_dashboard'),

    path('pmmu/', views.pmmu_list, name='pmmu_list'),
    path('pmmu/create/', views.pmmu_create, name='pmmu_create'),
    path('pmmu/<int:pk>/', views.pmmu_detail, name='pmmu_detail'),
    path('pmmu/<int:pk>/update/', views.pmmu_update, name='pmmu_update'),
    path('pmmu/<int:pk>/delete/', views.pmmu_delete, name='pmmu_delete'),

    path('indicator/', views.indicator_list, name='indicator_list'),
    path('indicator/create/pmmu/<int:pmmu_pk>/', views.indicator_create, name='indicator_create'), # Create indicator under a PMMU
    path('indicator/<int:pk>/', views.indicator_detail, name='indicator_detail'),
    path('indicator/<int:pk>/update/', views.indicator_update, name='indicator_update'),
    path('indicator/<int:pk>/delete/', views.indicator_delete, name='indicator_delete'),
    path('note/<int:note_id>/add-document/', views.add_note_document, name='add_note_document'),
    path('indicator/<int:indicator_id>/add-note/', views.add_indicator_note, name='add_indicator_note'),
]