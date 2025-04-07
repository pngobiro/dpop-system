# apps/statistics/views/unit_views.py
import os # Import os
import logging
from django.conf import settings # Import settings
from django.shortcuts import render, HttpResponse, redirect
from django_pandas.io import read_frame
import pandas as pd
from django.db.models import Count, Q, Sum
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)
from ..utils import get_dcrt_filepath # Import helper

logger = logging.getLogger(__name__)

def rank_unit_division_months(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    """View for displaying months for a specific unit and division."""
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=division_id)

    # Get months for the quarter
    months_in_quarter = Months.objects.filter(financial_quarter=fq.quarter_number).order_by('month_number')
    
    # Check file existence for each month
    months_data = []
    for month in months_in_quarter:
        file_path = get_dcrt_filepath(unit_rank, fy, month, unit)
        file_exists = os.path.exists(file_path) if file_path else False
        logger.debug(f"Checking for file for {month.name}: Path={file_path}, Exists={file_exists}")
        months_data.append({
            'month': month,
            'file_exists': file_exists
        })

    context = {
        'months_data': months_data, # Pass list of dicts with month and status
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
    }
    return render(request, 'statistics/rank_unit_months.html', context)

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

def unit_division_fy(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    """View for financial year statistics of a unit."""
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
    }
    return render(request, 'statistics/unit_division_fy.html', context)

def monthly_unit_matters_handled(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """
    View for analyzing matters handled in a specific month by a unit.
    Provides comprehensive analysis of case data.
    """
    try:
        # Get base objects
        unit_rank = UnitRank.objects.get(id=id)
        fy = FinancialYear.objects.get(id=financial_year_id)
        fq = FinancialQuarter.objects.get(id=financial_quarter_id)
        unit = Unit.objects.get(id=unit_id)
        division = Division.objects.get(id=division_id)
        month = Months.objects.get(id=month_id)

        # Get filtered queryset
        queryset = DcrtData.objects.filter(
            financial_year=financial_year_id,
            financial_quarter=financial_quarter_id,
            unit=unit_id,
            division=division_id,
            month=month_id
        )

        # Convert to dataframe for analysis
        df = read_frame(queryset)

        # Calculate case statistics
        context = {
            # Basic info
            'unit_rank': unit_rank,
            'financial_year': fy,
            'financial_quarter': fq,
            'unit': unit,
            'division': division,
            'month': month,

            # Main case statistics
            'case_stats': {
                'total_matters': len(df),
                'new_cases': len(df[df['case_outcome'].str.contains('Registered|Filed', na=False, case=False, regex=True)]) if not df.empty else 0,
                'resolved_cases': len(df[df['case_outcome'].str.contains('Resolved|Concluded|Completed', na=False, case=False, regex=True)]) if not df.empty else 0,
                'adjourned_cases': len(df[df['case_outcome'].str.contains('Adjourned', na=False, case=False)]) if not df.empty else 0
            },

            # Case type analysis
            'case_types': [
                {
                    'type': case_type,
                    'count': count,
                    'percentage': round(count/len(df)*100, 1) if len(df) > 0 else 0
                }
                for case_type, count in df['specific_case_type'].value_counts().items()
            ] if not df.empty else [],

            # Party statistics
            'party_stats': {
                'plaintiffs': {
                    'male': int(df['no_of_plaintiffs_or_appellants_male'].sum()),
                    'female': int(df['no_of_plaintiffs_or_appellants_female'].sum()),
                    'organizations': int(df['no_of_plaintiffs_or_appellants_organization'].sum())
                },
                'defendants': {
                    'male': int(df['no_of_defendants_accused_male'].sum()),
                    'female': int(df['no_of_defendants_accused_female'].sum()),
                    'organizations': int(df['no_of_defendants_accused_organization'].sum())
                }
            },

            # Witness statistics
            'witness_stats': {
                'total_witnesses': int(df['no_of_witnesses_in_court_d'].sum() + df['no_of_witnesses_in_court_w'].sum()),
                'defense_witnesses': int(df['no_of_witnesses_in_court_d'].sum()),
                'prosecution_witnesses': int(df['no_of_witnesses_in_court_w'].sum()),
                'cases_with_witnesses': len(df[(df['no_of_witnesses_in_court_d'] > 0) | (df['no_of_witnesses_in_court_w'] > 0)])
            },

            # Legal representation
            'representation_stats': {
                'with_lawyers': len(df[df['parties_have_legal_representation'].str.contains('Yes', na=False, case=False)]) if not df.empty else 0,
                'without_lawyers': len(df[df['parties_have_legal_representation'].str.contains('No', na=False, case=False)]) if not df.empty else 0,
                'not_specified': len(df[~df['parties_have_legal_representation'].str.contains('Yes|No', na=False, case=False, regex=True)]) if not df.empty else 0
            },

            # Remand statistics
            'remand_stats': {
                'total_remanded': int(df['no_of_accused_remanded'].sum()),
                'cases_with_remand': len(df[df['no_of_accused_remanded'] > 0])
            },

            # Next activity scheduling
            'next_activity': {
                'scheduled': len(df[df['date_of_next_activity_day'].notna()]),
                'not_scheduled': len(df[df['date_of_next_activity_day'].isna()])
            }
        }

        return render(request, 'statistics/monthly_unit_matters_handled.html', context)
        
    except (UnitRank.DoesNotExist, FinancialYear.DoesNotExist, 
            FinancialQuarter.DoesNotExist, Unit.DoesNotExist, 
            Division.DoesNotExist, Months.DoesNotExist) as e:
        return HttpResponse(f"Error: {str(e)}", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def upload_unit_monthly_dcrt_excel(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """Handle Excel file upload for monthly DCRT data."""
    from apps.statistics.utils import handle_uploaded_file
    
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=division_id)
    month = Months.objects.get(id=month_id)

    if request.method == 'POST':
        excel_file = request.FILES.get("excelFile") # Reverted name
        if excel_file:
            # Pass the actual objects to the utility function
            handle_uploaded_file(excel_file, unit_rank, fy, fq, unit, division, month)
            return redirect('statistics:monthly_unit_case_summary', id=id, financial_year_id=financial_year_id, 
                          financial_quarter_id=financial_quarter_id, unit_id=unit_id, division_id=division_id, month_id=month_id)
        return HttpResponse("No file uploaded.")

    context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,
    }
    return render(request, 'statistics/upload_unit_monthly_dcrt_excel.html', context)