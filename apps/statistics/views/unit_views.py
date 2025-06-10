# apps/statistics/views/unit_views.py
import os
import logging
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django_pandas.io import read_frame
import pandas as pd
from django.db.models import Count, Q, Sum
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)
from ..utils import get_dcrt_filepath

logger = logging.getLogger(__name__)

def rank_unit_division_months(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    """View for displaying months for a specific unit and division."""
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=division_id)
    logger.info(f"Unit: {unit.name} (ID: {unit.id}, DCRT ID: {getattr(unit, 'dcrt_unique_id', None)})")
    logger.info(f"Division: {division.name} (ID: {division.id})")
    logger.info(f"Request Parameters - rank: {id}, fy: {financial_year_id}, fq: {financial_quarter_id}, unit: {unit_id}, division: {division_id}")

    # Get months for the quarter
    months_in_quarter = Months.objects.filter(financial_quarter=fq.quarter_number).order_by('month_number')
    logger.info(f"Found {months_in_quarter.count()} months for quarter {fq.quarter_number}")
    for m in months_in_quarter:
        logger.info(f"Month: {m.name} (ID: {m.id}, Number: {m.month_number})")
    
    import glob
    
    # Base DCRT directory
    dcrt_base = os.path.join(settings.BASE_DIR, 'DCRT')
    logger.info(f"Base DCRT directory: {dcrt_base}")
    logger.info(f"Looking for files for unit: {unit.name} (rank: {unit_rank.name})")
    logger.info(f"DCRT Unique ID: {getattr(unit, 'dcrt_unique_id', 'Not set')}")
    logger.info(f"Financial Year: {fy.name}, Quarter: {fq.quarter_number}, Division: {division.name}")

    # Check file existence for each month
    months_data = []

    for month in months_in_quarter:
        file_exists = False
        month_str = f"{month.month_number:02d}"
        year_str = fy.name.split('/')[0]  # Just get first year

        # Determine the template folder based on unit_rank.id
        template_folder = 4 if unit_rank.id == 4 or unit_rank.id == 5 else unit_rank.id

        # Get the unit's DCRT unique ID
        dcrt_unique_id = getattr(unit, 'dcrt_unique_id', None)
        
        # Construct the file pattern based on DCRT directory structure
        unit_pattern = os.path.join(
            dcrt_base,
            f"TEMPLATE {template_folder}",
            f"{unit.name}*",  # Allow for variations in court names
            year_str,
            f"{month_str:0>2}",  # Ensure two digit month
            "*.xlsx"  # First try any Excel file
        )
        logger.info(f"Searching for DCRT files with pattern: {unit_pattern}")
        logger.info(f"Checking unit pattern: {unit_pattern}")

        matching_files = glob.glob(unit_pattern)
        if matching_files:
            file_exists = True
            found_file = matching_files[0]
            logger.info(f"✓ Found file in unit directory: {found_file}")
            logger.info(f"  - File exists at: {os.path.abspath(found_file)}")
            logger.info(f"  - Month: {month.name} ({month_str})")

        if not file_exists:
            # Try looking in any subdirectory under the template folder
            template_pattern = os.path.join(
                dcrt_base,
                f"TEMPLATE {template_folder}",
                "*",  # Any court directory
                year_str,
                f"{month_str:0>2}",  # Ensure two digit month
                "*.xlsx"
            )
            logger.info(f"Checking template pattern with DCRT ID: {template_pattern}")
            
            matching_templates = glob.glob(template_pattern)
            if matching_templates:
                file_exists = True
                found_file = matching_templates[0]
                template_court = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(found_file))))
                logger.info(f"✓ Found file with DCRT ID {unit.dcrt_unique_id} in {template_court}: {found_file}")
            
        if not file_exists:
            logger.info("✗ No files found for this month")
        
        logger.debug(f"Month {month.name}: File exists = {file_exists}")
        # Add details to months_data
        months_data.append({
            'month': month,
            'month_number': month_str,
            'month_id': month.id,  # Explicitly include month.id
            'file_exists': file_exists,
            'template_path': os.path.join(
                f"TEMPLATE {template_folder}",
                unit.name,
                year_str,
                month_str,
                f"{unit.dcrt_unique_id}.xlsx" if unit.dcrt_unique_id else "*.xlsx"
            ),
            'dcrt_id': unit.dcrt_unique_id
        })

    # Log division info before creating context
    logger.info("Division object details:")
    logger.info(f"- Name: {division.name}")
    logger.info(f"- ID: {division.id}")
    logger.info(f"- Dict: {division.__dict__}")
    
    context = {
        'months_data': months_data,
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,  # This should have a valid ID
        'template_base': f"TEMPLATE {unit_rank.id}/{unit.name}",  # For display purposes
        'division_id': division.id,  # Explicitly add division_id to context
    }
    
    # Log final results
    logger.info("\nFinal Results:")
    for month_data in months_data:
        status = "✓ Found" if month_data['file_exists'] else "✗ Missing"
        logger.info(f"{month_data['month'].name}: {status}")

    logger.info(f"Months data: {months_data}")

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
            division_id_safe = int(division_id) if division_id else 0
            return redirect('statistics:monthly_unit_case_summary', id=id, financial_year_id=financial_year_id,
                          financial_quarter_id=financial_quarter_id, unit_id=unit_id, division_id=division_id_safe, month_id=month_id)
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