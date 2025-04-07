from django.shortcuts import render
from django.db import models # Import models
from django.db.models import Count, Q
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months, UnitDivision # Added UnitDivision
)

def home(request):
    """
    Dashboard view showing overall statistics and navigation options.
    """
    context = {
        'unit_ranks': UnitRank.objects.all(),
        'total_units': Unit.objects.count(),
        'active_divisions': Division.objects.filter(is_active=True).count(),
        'court_units': Unit.objects.filter(is_court=True).count(),
        'financial_year': FinancialYear.objects.first(),
        'financial_quarter': FinancialQuarter.objects.first(),
        
        # Add summary statistics
        'total_cases': DcrtData.objects.count(),
        'resolved_cases': DcrtData.objects.filter(
            case_outcome__icontains='Resolved'
        ).count(),
        'pending_cases': DcrtData.objects.exclude(
            case_outcome__icontains='Resolved'
        ).count(),
        
        # Get top case types
        'top_case_types': DcrtData.objects.values(
            'specific_case_type'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5],
    }
    return render(request, 'statistics/home.html', context)

def rank_units(request, id, financial_year_id, financial_quarter_id):
    """
    View for displaying units within a specific rank.
    """
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)

    # Get all units for the given rank
    # Prefetch all associated divisions via the UnitDivision intermediate model
    units_with_divisions = Unit.objects.filter(unit_rank=id).prefetch_related(
        models.Prefetch(
            'unitdivision_set', # Default related name for UnitDivision back to Unit
            queryset=UnitDivision.objects.select_related('division'), # Fetch Division info efficiently
            to_attr='unit_divisions_prefetch' # Store prefetched objects here
        )
    ).order_by('name')

    # Structure data for template (extract divisions from prefetch)
    units_data = []
    for unit in units_with_divisions:
        # Extract prefetched divisions
        divisions = [ud.division for ud in unit.unit_divisions_prefetch]
        units_data.append({
            'unit': unit,
            'divisions': divisions
        })

    context = {
        'units_data': units_data, # Pass processed data
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
    }
    return render(request, 'statistics/rank_units.html', context)