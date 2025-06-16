from django.shortcuts import render
from apps.statistics.models import FinancialYear, FinancialQuarter

def unit_division_quarters(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    """View for quarterly statistics of a unit."""
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
        'division_id': division_id,
    }
    return render(request, 'statistics/unit_division_quarters.html', context)