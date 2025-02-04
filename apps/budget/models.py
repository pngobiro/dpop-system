# apps/budget/models.py
from django.db import models

class BudgetCategory(models.Model):
    """Budget category/heading"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Budget Categories"

class FinancialYear(models.Model):
    """Financial Year"""
    name = models.CharField(max_length=20)  # e.g. 2021/22
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name

class WorkplanItem(models.Model):
    """Main workplan item"""
    ITEM_TYPES = [
        ('regular', 'Regular Activity'),
        ('transformative', 'Transformative Initiative')
    ]
    
    name = models.CharField(max_length=255)
    budget_code = models.CharField(max_length=20)  # e.g. 2211002
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.budget_code})"

class QuarterlyAllocation(models.Model):
    """Quarterly budget allocations"""
    workplan_item = models.ForeignKey(WorkplanItem, on_delete=models.CASCADE)
    quarter = models.IntegerField(choices=[(1,'Q1'),(2,'Q2'),(3,'Q3'),(4,'Q4')])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        unique_together = ['workplan_item', 'quarter']

class PerformanceIndicator(models.Model):
    """KPIs and performance measures"""
    workplan_item = models.ForeignKey(WorkplanItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    baseline = models.CharField(max_length=100, blank=True)
    target = models.CharField(max_length=100)
    measurement_frequency = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} - {self.workplan_item.name}"

class TransformativeInitiative(models.Model):
    """Key transformative initiatives"""
    workplan_item = models.OneToOneField(
        WorkplanItem, 
        on_delete=models.CASCADE,
        limit_choices_to={'item_type': 'transformative'}
    )
    implementation_status = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    progress = models.IntegerField(default=0)  # 0-100%
    
    def __str__(self):
        return f"Initiative: {self.workplan_item.name}"