# apps/organization/models.py
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Role(models.Model):
    JOB_GROUPS = [
        ('JSG1', 'JSG1'),
        ('JSG2', 'JSG2'),
        ('JSG3', 'JSG3'),
        ('JSG4', 'JSG4'),
        ('JSG5', 'JSG5'),
    ]

    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='roles')
    job_group = models.CharField(max_length=4, choices=JOB_GROUPS)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.department.name})"

    class Meta:
        ordering = ['department', 'job_group', 'title']

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.title}"

    class Meta:
        unique_together = ['user', 'role']