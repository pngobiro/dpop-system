from django.urls import path
from apps.courses.views import CourseDetailView
from .views import CourseListView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
]
