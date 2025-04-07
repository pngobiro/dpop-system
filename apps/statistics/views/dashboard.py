import json
import logging
from collections import defaultdict
from django.shortcuts import render
from django.db import models
from django.db.models import Count, Q
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months, UnitDivision
)

# Configure logger with more detailed format
logger = logging.getLogger(__name__)

def home(request):
    """
    Dashboard view showing overall statistics and navigation options.
    """
    # Prepare data for dropdowns
    unit_ranks = UnitRank.objects.all()
    financial_years = FinancialYear.objects.all().order_by('-name')

    # Prepare all quarters grouped by financial year ID for JavaScript
    all_quarters = FinancialQuarter.objects.order_by('financial_year_id', 'quarter_number')
    quarters_by_year = defaultdict(list)
    for quarter in all_quarters:
        quarters_by_year[quarter.financial_year_id].append({
            'id': quarter.id,
            'name': quarter.get_quarter_name() # Use the formatted name
        })
    all_quarters_json = json.dumps(dict(quarters_by_year))

    # Summary statistics (keep existing logic)
    total_units = Unit.objects.count()
    active_divisions = Division.objects.filter(is_active=True).count()
    total_cases = DcrtData.objects.count()
    resolved_cases = DcrtData.objects.filter(case_outcome__icontains='Resolved').count()

    context = {
        'unit_ranks': unit_ranks,
        'financial_years': financial_years,
        'all_quarters_json': all_quarters_json, # Pass JSON data to template
        'total_units': total_units,
        'active_divisions': active_divisions,
        'total_cases': total_cases,
        'resolved_cases': resolved_cases,
        # Add other stats if needed
    }
    return render(request, 'statistics/home.html', context)
def rank_units(request, id, financial_year_id, financial_quarter_id):
    """View for displaying units within a specific rank."""
    print(f"\n=== rank_units view called ===")
    print(f"Parameters: rank_id={id}, fy_id={financial_year_id}, fq_id={financial_quarter_id}")
    
    try:
        # Get and log UnitRank details
        unit_rank = UnitRank.objects.get(id=id)
        print(f"Found UnitRank: {unit_rank.name} (id={unit_rank.id})")
        
        # Get and log FinancialYear details
        fy = FinancialYear.objects.get(id=financial_year_id)
        print(f"Found FinancialYear: {fy.name} (id={fy.id})")
        
        # Get and log FinancialQuarter details
        fq = FinancialQuarter.objects.get(id=financial_quarter_id)
        print(f"Found FinancialQuarter: {fq.name} (id={fq.id})")
        logger.info(f"Found FinancialQuarter: {fq.name} (id={fq.id})")

        # First, check total units for this rank without any filtering
        total_units = Unit.objects.filter(unit_rank=id).count()
        print(f"\nTotal units found for rank {unit_rank.name}: {total_units}")
        print(f"SQL: {Unit.objects.filter(unit_rank=id).query}")

        # Get all units for the given rank with prefetched divisions
        units_qs = Unit.objects.filter(unit_rank=id).select_related('unit_rank').prefetch_related(
            models.Prefetch(
                'unitdivision_set',
                queryset=UnitDivision.objects.select_related('division'),
                to_attr='unit_divisions_prefetch'
            )
        ).order_by('name')

        # Log the query and results
        print(f"\nFull query SQL: {units_qs.query}")
        print(f"Units found: {units_qs.count()}")
        
        # Build units data structure
        units_data = []
        for unit in units_qs:
            divisions = [ud.division for ud in getattr(unit, 'unit_divisions_prefetch', [])]
            print(f"Processing unit: {unit.name} ({unit.unit_rank.name if unit.unit_rank else 'No rank'})")
            units_data.append({
                'unit': unit,
                'divisions': divisions
            })
            print(f"- Found {len(divisions)} divisions")
        
        print(f"\nProcessed {len(units_data)} total units")

        context = {
            'units_data': units_data,
            'units': units_data,  # Add for backward compatibility with template
            'unit_rank': unit_rank,
            'financial_year': fy,
            'financial_quarter': fq,
        }
        
        logger.info(f"Rendering template with {len(units_data)} units")
        return render(request, 'statistics/rank_units.html', context)

    except UnitRank.DoesNotExist:
        logger.error(f"UnitRank with id={id} not found")
        raise
    except FinancialYear.DoesNotExist:
        logger.error(f"FinancialYear with id={financial_year_id} not found")
        raise
    except FinancialQuarter.DoesNotExist:
        logger.error(f"FinancialQuarter with id={financial_quarter_id} not found")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in rank_units view: {str(e)}")
        raise