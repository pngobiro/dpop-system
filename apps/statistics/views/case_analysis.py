import pandas as pd
import os # Import os module
import openpyxl # Import openpyxl
from django.conf import settings # Import settings
from django.shortcuts import render
from django_pandas.io import read_frame
from django.db.models import Count, Q
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)
from ..utils import get_dcrt_filepath # Import the helper function
import logging

logger = logging.getLogger(__name__)

def case_summary(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """
    Comprehensive case summary and analysis view.
    """
    # Get base objects
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=division_id)
    month = Months.objects.get(id=month_id)

    df = pd.DataFrame() # Initialize empty DataFrame
    data_source = "Database" # Default source

    # Construct the expected filepath
    filepath = get_dcrt_filepath(unit_rank, fy, month, unit)

    if filepath and os.path.exists(filepath):
        logger.info(f"Found existing Excel file for case summary: {filepath}")
        try:
            # Read data directly from the Excel file using pandas
            # Adjust sheet_name and header row if needed based on template
            df = pd.read_excel(filepath, sheet_name=0, header=4) # Assumes data starts on row 6 (header=4 means 5th row is header)
            df = df.where(pd.notnull(df), None) # Replace NaN with None
            data_source = "Excel File"
            logger.info(f"Successfully loaded {len(df)} rows from Excel file.")
        except Exception as e:
            logger.error(f"Error reading Excel file {filepath}: {e}. Falling back to database.")
            df = pd.DataFrame() # Ensure df is empty on read error

    # If file doesn't exist or failed to read, query the database
    if df.empty:
        logger.info("Excel file not found or failed to read. Querying database.")
        queryset = DcrtData.objects.filter(
            financial_year=financial_year_id,
            # financial_quarter=financial_quarter_id, # Quarter info is in Month object
            unit=unit_id,
            division=division_id,
            month=month_id
        )
        if queryset.exists():
            df = read_frame(queryset)
            df = df.where(pd.notnull(df), None)
            logger.info(f"Successfully loaded {len(df)} rows from database.")
        else:
            logger.info("No data found in database for this context.")
            # df remains an empty DataFrame

    context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'data_source': data_source, # Add data source info to context
        'month': month,
        
        # Basic statistics
        'total_cases': len(df),
        'resolved_cases': len(df[df['case_outcome'].str.contains('Resolved|Concluded|Completed', na=False, case=False, regex=True)]) if not df.empty and 'case_outcome' in df.columns else 0,
        'pending_cases': len(df[~df['case_outcome'].str.contains('Resolved|Concluded|Completed', na=False, case=False, regex=True)]) if not df.empty and 'case_outcome' in df.columns else len(df), # Assume all are pending if outcome column missing
        'legal_rep_cases': len(df[df['parties_have_legal_representation'].str.contains('Yes', na=False, case=False)]) if not df.empty and 'parties_have_legal_representation' in df.columns else 0,
        
        # Case types analysis
        'case_types': [
            {
                'type': case_type,
                'count': count,
                'percentage': round(count/len(df)*100, 1) if len(df) > 0 else 0
            }
            for case_type, count in (df['specific_case_type'].value_counts().items() if 'specific_case_type' in df.columns else [])
        ] if not df.empty else [],
        
        # Case outcomes analysis
        'case_outcomes': [
            {
                'type': outcome,
                'count': count,
                'percentage': round(count/len(df)*100, 1) if len(df) > 0 else 0
            }
            for outcome, count in (df['case_outcome'].value_counts().items() if 'case_outcome' in df.columns else [])
        ] if not df.empty else [],
        
        # Demographics
        'plaintiff_stats': {
            'male': int(df['no_of_plaintiffs_or_appellants_male'].sum()) if not df.empty and 'no_of_plaintiffs_or_appellants_male' in df.columns else 0,
            'female': int(df['no_of_plaintiffs_or_appellants_female'].sum()) if not df.empty and 'no_of_plaintiffs_or_appellants_female' in df.columns else 0,
            'org': int(df['no_of_plaintiffs_or_appellants_organization'].sum()) if not df.empty and 'no_of_plaintiffs_or_appellants_organization' in df.columns else 0,
        },
        'defendant_stats': {
            'male': int(df['no_of_defendants_accused_male'].sum()) if not df.empty and 'no_of_defendants_accused_male' in df.columns else 0,
            'female': int(df['no_of_defendants_accused_female'].sum()) if not df.empty and 'no_of_defendants_accused_female' in df.columns else 0,
            'org': int(df['no_of_defendants_accused_organization'].sum()) if not df.empty and 'no_of_defendants_accused_organization' in df.columns else 0,
        },
    }
    
    return render(request, 'statistics/case_summary.html', context)

def monthly_unit_registered_cases(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """
    View for analyzing registered cases in a given month.
    """
    queryset = DcrtData.objects.filter(
        financial_year=financial_year_id,
        financial_quarter=financial_quarter_id,
        unit=unit_id,
        division=division_id,
        month=month_id,
        case_outcome__icontains='Case Registered/Filed'
    )
    
    df = read_frame(queryset)
    
    context = {
        'registered_cases': len(df),
        'registered_cases_by_type': df.groupby('case_number_code').size().to_dict(),
        'basic_info': {
            'unit_rank': UnitRank.objects.get(id=id),
            'financial_year': FinancialYear.objects.get(id=financial_year_id),
            'financial_quarter': FinancialQuarter.objects.get(id=financial_quarter_id),
            'unit': Unit.objects.get(id=unit_id),
            'division': Division.objects.get(id=division_id),
            'month': Months.objects.get(id=month_id),
        }
    }
    
    return render(request, 'statistics/monthly_unit_registered_cases.html', context)


def monthly_unit_resolved_cases(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """
    View for analyzing resolved cases in a given month.
    """
    queryset = DcrtData.objects.filter(
        financial_year=financial_year_id,
        financial_quarter=financial_quarter_id,
        unit=unit_id,
        division=division_id,
        month=month_id,
        case_outcome__icontains='Resolved'
    )
    
    df = read_frame(queryset)
    
    context = {
        'resolved_cases': len(df),
        'resolved_cases_by_type': df.groupby('case_number_code').size().to_dict(),
        'basic_info': {
            'unit_rank': UnitRank.objects.get(id=id),
            'financial_year': FinancialYear.objects.get(id=financial_year_id),
            'financial_quarter': FinancialQuarter.objects.get(id=financial_quarter_id),
            'unit': Unit.objects.get(id=unit_id),
            'division': Division.objects.get(id=division_id),
            'month': Months.objects.get(id=month_id),
        }
    }
    
    return render(request, 'statistics/monthly_unit_resolved_cases.html', context)


def rank_unit_division_month_cases_summary(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """
    View for ranking unit-division-month cases summary.
    """
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

    context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,

        # Basic statistics
        'total_cases': len(df),
        'resolved_cases': len(df[df['case_outcome'].str.contains(
            'Resolved|Concluded|Completed', na=False, case=False, regex=True
        )]),
        'pending_cases': len(df[~df['case_outcome'].str.contains(
            'Resolved|Concluded|Completed', na=False, case=False, regex=True
        )]),

        # Case types analysis
        'case_types': [
            {
                'type': case_type,
                'count': count,
                'percentage': round(count/len(df)*100, 1)
            }
            for case_type, count in df['specific_case_type'].value_counts().items()
        ],

        # Demographics
        'plaintiff_stats': {
            'male': df['no_of_plaintiffs_or_appellants_male'].sum(),
            'female': df['no_of_plaintiffs_or_appellants_female'].sum(),
            'org': df['no_of_plaintiffs_or_appellants_organization'].sum(),
            'total': df['no_of_plaintiffs_or_appellants_male'].sum() + 
                    df['no_of_plaintiffs_or_appellants_female'].sum() +
                    df['no_of_plaintiffs_or_appellants_organization'].sum()
        },
        'defendant_stats': {
            'male': df['no_of_defendants_accused_male'].sum(),
            'female': df['no_of_defendants_accused_female'].sum(),
            'org': df['no_of_defendants_accused_organization'].sum(),
            'total': df['no_of_defendants_accused_male'].sum() +
                    df['no_of_defendants_accused_female'].sum() +
                    df['no_of_defendants_accused_organization'].sum()
        },

        # Legal representation
        'legal_representation': {
            'with_representation': len(df[df['parties_have_legal_representation'].str.contains('Yes', na=False, case=False)]),
            'without_representation': len(df[df['parties_have_legal_representation'].str.contains('No', na=False, case=False)]),
            'not_specified': len(df[~df['parties_have_legal_representation'].str.contains('Yes|No', na=False, case=False, regex=True)])
        },

        # Witness statistics
        'witness_stats': {
            'defense': df['no_of_witnesses_in_court_d'].sum(),
            'prosecution': df['no_of_witnesses_in_court_w'].sum(),
            'total': df['no_of_witnesses_in_court_d'].sum() + df['no_of_witnesses_in_court_w'].sum()
        },

        # Additional case statistics
        'remand_stats': {
            'total_remanded': df['no_of_accused_remanded'].sum(),
            'cases_with_remand': len(df[df['no_of_accused_remanded'] > 0])
        }
    }

    return render(request, 'statistics/rank_unit_division_month_cases_summary.html', context)


def monthly_unit_matters_handled(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """
    View for analyzing matters handled in a specific month by a unit.
    Shows various case statistics and breakdowns.
    """
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

    # Calculate matters handled statistics
    context = {
        # Basic info
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,

        # Case statistics
        'case_stats': {
            'total_matters': len(df),
            'new_cases': len(df[df['case_outcome'].str.contains('Registered|Filed', na=False, case=False, regex=True)]),
            'resolved_cases': len(df[df['case_outcome'].str.contains('Resolved|Concluded|Completed', na=False, case=False, regex=True)]),
            'adjourned_cases': len(df[df['case_outcome'].str.contains('Adjourned', na=False, case=False)])
        },

        # Case types breakdown
        'case_types': [
            {
                'type': case_type,
                'count': count,
                'percentage': round(count/len(df)*100, 1) if len(df) > 0 else 0
            }
            for case_type, count in df['specific_case_type'].value_counts().items()
        ],

        # Coming for analysis
        'coming_for_analysis': [
            {
                'reason': reason,
                'count': count,
                'percentage': round(count/len(df)*100, 1) if len(df) > 0 else 0
            }
            for reason, count in df['case_coming_for'].value_counts().items()
        ],

        # Adjournment reasons
        'adjournment_reasons': [
            {
                'reason': reason,
                'count': count,
                'percentage': round(count/len(df)*100, 1) if len(df) > 0 else 0
            }
            for reason, count in df['adjournment_reason'].value_counts().items()
            if not pd.isna(reason)
        ],

        # Judicial officer workload
        'judicial_workload': {
            'officers_involved': len(df[[f'judicial_officer_{i}' for i in range(1, 9)]].notna().any(axis=1)),
            'cases_per_officer': round(len(df) / len(df[[f'judicial_officer_{i}' for i in range(1, 9)]].notna().any(axis=1)), 2)
            if len(df[[f'judicial_officer_{i}' for i in range(1, 9)]].notna().any(axis=1)) > 0 else 0
        },

        # Representation statistics
        'representation_stats': {
            'with_lawyers': len(df[df['parties_have_legal_representation'].str.contains('Yes', na=False, case=False)]),
            'without_lawyers': len(df[df['parties_have_legal_representation'].str.contains('No', na=False, case=False)]),
            'not_specified': len(df[~df['parties_have_legal_representation'].str.contains('Yes|No', na=False, case=False, regex=True)])
        },

        # Party statistics
        'party_stats': {
            'plaintiffs': {
                'male': df['no_of_plaintiffs_or_appellants_male'].sum(),
                'female': df['no_of_plaintiffs_or_appellants_female'].sum(),
                'organizations': df['no_of_plaintiffs_or_appellants_organization'].sum()
            },
            'defendants': {
                'male': df['no_of_defendants_accused_male'].sum(),
                'female': df['no_of_defendants_accused_female'].sum(),
                'organizations': df['no_of_defendants_accused_organization'].sum()
            }
        },

        # Witness participation
        'witness_stats': {
            'total_witnesses': df['no_of_witnesses_in_court_d'].sum() + df['no_of_witnesses_in_court_w'].sum(),
            'defense_witnesses': df['no_of_witnesses_in_court_d'].sum(),
            'prosecution_witnesses': df['no_of_witnesses_in_court_w'].sum(),
            'cases_with_witnesses': len(df[(df['no_of_witnesses_in_court_d'] > 0) | (df['no_of_witnesses_in_court_w'] > 0)])
        },

        # Next activity analysis
        'next_activity': {
            'scheduled': len(df[df['date_of_next_activity_day'].notna()]),
            'not_scheduled': len(df[df['date_of_next_activity_day'].isna()]),
        },

        # Remand cases
        'remand_stats': {
            'total_remanded': df['no_of_accused_remanded'].sum(),
            'cases_with_remand': len(df[df['no_of_accused_remanded'] > 0])
        }
    }

    return render(request, 'statistics/monthly_unit_matters_handled.html', context)

