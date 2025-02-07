# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from apps.organization.models import Department


class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-file-alt')")
    url_name = models.CharField(max_length=200, blank=True, help_text="Name of the URL pattern for this module (e.g., 'document_module_view')")
    departments = models.ManyToManyField(Department, related_name='modules', blank=True)  # Changed to ManyToManyField
    permission_codename = models.CharField(max_length=150, unique=True, blank=True, help_text="Codename for permission to access this module (e.g., 'access_documents')")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []  # Custom permissions handled by seeder