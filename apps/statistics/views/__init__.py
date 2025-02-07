from django.shortcuts import render
from django.db.models import Count
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)

def home(request):
    """Dashboard view showing overall statistics and navigation options."""
    context = {
        'unit_ranks': UnitRank.objects.all(),
        'total_units': Unit.objects.count(),
        'active_divisions': Division.objects.filter(is_active=True).count(),
        'court_units': Unit.objects.filter(is_court=True).count(),
        'financial_year': FinancialYear.objects.first(),
        'financial_quarter': FinancialQuarter.objects.first(),
        
        # Additional statistics
        'total_cases': DcrtData.objects.count(),
        'resolved_cases': DcrtData.objects.filter(
            case_outcome__icontains='Resolved'
        ).count(),
        'pending_cases': DcrtData.objects.exclude(
            case_outcome__icontains='Resolved'
        ).count(),
        
        # Top case types
        'top_case_types': DcrtData.objects.values(
            'specific_case_type'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5],
    }
    return render(request, 'statistics/home.html', context)

# Import views from modules
from .dashboard import (
    rank_units,
)

from .case_analysis import (
    case_summary,
    monthly_unit_registered_cases,
    monthly_unit_resolved_cases,
    rank_unit_division_month_cases_summary,
)

from .unit_views import (
    rank_unit_division_months,
    unit_division_quarters,
    unit_division_fy,
    monthly_unit_matters_handled,
    upload_unit_monthly_dcrt_excel,
)

from .data_quality import (
    monthly_unit_missing_data,
    monthly_unit_duplicate_data,
    monthly_unit_outliers,
    monthly_unit_incomplete_data,
)

# Export all views
__all__ = [
    # Main view
    'home',
    
    # Dashboard views
    'rank_units',
    
    # Case analysis views
    'case_summary',
    'monthly_unit_registered_cases',
    'monthly_unit_resolved_cases',
    'rank_unit_division_month_cases_summary',
    
    # Unit views
    'rank_unit_division_months',
    'unit_division_quarters',
    'unit_division_fy',
    'monthly_unit_matters_handled',
    'upload_unit_monthly_dcrt_excel',
    
    # Data quality views
    'monthly_unit_missing_data',
    'monthly_unit_duplicate_data',
    'monthly_unit_outliers',
    'monthly_unit_incomplete_data',
]