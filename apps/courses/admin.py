from django.contrib import admin
from apps.courses.models import Course
from apps.courses.models import PastPaper
from apps.courses.models import Subject

class PastPaperInline(admin.TabularInline):
    model = PastPaper

class SubjectInline(admin.TabularInline):
    model = Subject    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [PastPaperInline, SubjectInline]
