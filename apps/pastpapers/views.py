
from django.views.generic import DetailView
from .models import Course




class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'


    
