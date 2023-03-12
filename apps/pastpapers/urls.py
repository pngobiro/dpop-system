from django.urls import path
from .views import CourseDetailView, PastPaperListView, PastPaperDetailView


app_name = 'apps.pastpapers'

urlpatterns = [
    path('', PastPaperListView.as_view(), name='pastpaper_list'),
    path('<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:course_id>/pastpapers/', PastPaperListView.as_view(), name='course_pastpaper_list'),
    path('<int:course_id>/pastpapers/<int:pastpaper_id>/', PastPaperDetailView.as_view(), name='pastpaper_detail'),
]