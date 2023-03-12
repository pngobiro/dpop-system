from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PastPaper(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='past_papers')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    objects = models.Manager()  # specify the default manager

    def __str__(self):
        return self.name


    def past_papers(self):
        return PastPaper.objects.filter(course=self)
        
class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    is_deleted = models.BooleanField(default=False)


class Question(models.Model):
    course = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number = models.IntegerField()
    order  = models.IntegerField()
    is_published = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    
