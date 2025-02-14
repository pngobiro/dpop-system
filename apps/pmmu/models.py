# apps/pmmu/models.py
from django.db import models
from apps.statistics.models import FinancialYear
from apps.organization.models import Department
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from apps.document_management.models import Document

class IndicatorCategory(models.Model):
    """Represents a category for Performance Indicators (e.g., CORE MANDATE)."""
    name = models.CharField(max_length=255, unique=True, help_text="Unique name of the indicator category (e.g., core_mandate - used internally)")
    display_name = models.CharField(max_length=255, blank=True, help_text="User-friendly display name (e.g., A. CORE MANDATE - shown to users, optional)")
    description = models.TextField(blank=True, help_text="Optional description of the category")

    class Meta:
        verbose_name = "Indicator Category"
        verbose_name_plural = "Indicator Categories"
        ordering = ['name']

    def __str__(self):
        return self.display_name if self.display_name else self.name


class PMMU(models.Model):
    """Represents the overall Performance Management & Measurement Understanding document."""
    name = models.CharField(max_length=255, help_text="Name of the PMMU document (e.g., PMMU Understanding 2024-2025)")
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='pmmus', help_text="Financial Year this PMMU applies to")
    description = models.TextField(blank=True, help_text="Optional description of the PMMU document")
    documents = GenericRelation(Document)  # Attach documents to the PMMU itself
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.financial_year.name})"

    class Meta:
        verbose_name = "PMMU Understanding"
        verbose_name_plural = "PMMU Understandings"
        ordering = ['-financial_year', '-created_at']


class PerformanceIndicator(models.Model):
    """Represents a specific, measurable performance indicator (definition - year-agnostic)."""
    subcategory = models.ForeignKey(IndicatorCategory, on_delete=models.SET_NULL, null=True, related_name='indicators', help_text="Category this indicator belongs to")
    description = models.TextField(blank=True, help_text="Optional description of the indicator")
    name = models.TextField(help_text="Description of the performance indicator (e.g., Institutionalize Performance Management)")
    unit_of_measure = models.CharField(max_length=50, help_text="Unit of measurement (e.g., %, No.)")
    weight = models.IntegerField(default=0, help_text="Weight or importance of this indicator in percentage (e.g., 10)")

    class Meta:
        verbose_name = "Performance Indicator"
        verbose_name_plural = "Performance Indicators"
        ordering = ['subcategory__name', 'name'] # Order by category name then indicator name

    def __str__(self):
        return f"{self.name} ({self.subcategory})"


class FinancialYearPerformance(models.Model):
    """Stores performance data for each indicator for each financial year."""
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='performance_data', help_text="Financial Year for this performance data")
    indicator = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE, related_name='financial_year_data', help_text="Performance Indicator")
    target = models.CharField(max_length=100, help_text="Target performance for this financial year")
    baseline = models.CharField(max_length=100, blank=True, null=True, help_text="Baseline performance for this financial year (could be from previous FY)")
    actual = models.CharField(max_length=100, blank=True, null=True, help_text="Actual performance achieved in this financial year")

    class Meta:
        verbose_name = "Financial Year Performance Data"
        verbose_name_plural = "Financial Year Performance Data"
        unique_together = ['financial_year', 'indicator'] # One performance entry per indicator per FY
        ordering = ['financial_year', 'indicator__subcategory__name', 'indicator__name'] # Order by FY, Category, then Indicator

    def __str__(self):
        return f"{self.indicator.name} - {self.financial_year}"


class IndicatorNote(models.Model):
    """Represents notes associated with a Performance Indicator."""
    indicator = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField(help_text="Text content of the note")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="User who created the note")
    documents = GenericRelation(Document) # Documents attached to notes

    def __str__(self):
        return f"Note for {self.indicator.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Indicator Note"
        verbose_name_plural = "Indicator Notes"
        ordering = ['-created_at']