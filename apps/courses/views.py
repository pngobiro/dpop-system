from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'



class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

