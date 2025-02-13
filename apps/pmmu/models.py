# apps/pmmu/models.py
from django.db import models
from apps.statistics.models import FinancialYear
from apps.organization.models import Department
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from apps.document_management.models import Document

class PMMU(models.Model):
    """Represents the overall Performance Management & Measurement Understanding document."""
    name = models.CharField(max_length=255) # e.g., "PMMU Understanding 2024-2025"
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='pmmus')
    description = models.TextField(blank=True)
    documents = GenericRelation(Document)  # Attach documents to the PMMU itself
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.financial_year.name})"

    class Meta:
        verbose_name = "PMMU Understanding"
        verbose_name_plural = "PMMU Understandings"
        ordering = ['-financial_year', '-created_at']


class Indicator(models.Model):
    """Represents a Performance Indicator for a PMMU."""
    pmmu = models.ForeignKey(PMMU, on_delete=models.CASCADE, related_name='indicators') # ForeignKey to PMMU
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='indicators') # Keep Department for context
    unit_of_measure = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(default=0)
    baseline_2023_2024 = models.CharField(max_length=100, blank=True)
    target_2024_2025 = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True) # ADDED DESCRIPTION FIELD BACK HERE
    notes = GenericRelation(Document) # Documents directly attached to Indicator - if needed, remove if docs only at Note level

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_indicators')

    def __str__(self):
        return f"{self.name} for {self.pmmu.name}" # Updated str representation

    class Meta:
        verbose_name = "Performance Indicator"
        verbose_name_plural = "Performance Indicators"
        ordering = ['-created_at']


class IndicatorNote(models.Model):
    """Represents notes associated with a Performance Indicator."""
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    documents = GenericRelation(Document) # Documents attached to notes, as before

    def __str__(self):
        return f"Note for {self.indicator.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Indicator Note"
        verbose_name_plural = "Indicator Notes"
        ordering = ['-created_at']