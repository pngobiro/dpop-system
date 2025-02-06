      
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.organization.models import Department  # Correct import path


class CustomUser(AbstractUser):
    departments = models.ManyToManyField(Department, related_name='members')

    # Add any other fields you need here, e.g.
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    pj_number = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=150, blank=True)


    # OPTIONAL: Add a __str__ method
    def __str__(self):
        return self.username

    @property
    def department(self):
        """Get user's primary department based on their active role"""
        user_role = self.user_roles.filter(is_active=True).first()
        if user_role:
            return user_role.role.department
        return None
    
    @property
    def is_director(self):
        """Check if user is a director"""
        return self.user_roles.filter(is_active=True, role__name='Director').exists()

    @property
    def is_manager(self):
        """Check if user is a manager"""
        return self.user_roles.filter(is_active=True, role__name='Manager').exists()