from django.db import models

# Create your models here.

from django.db import models

class UnitRank(models.Model):
    name = models.CharField(max_length=255)
    is_court = models.BooleanField(default=False)

class FinancialYear(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class FinancialQuarter(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)


