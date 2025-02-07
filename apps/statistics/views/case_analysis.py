from django.shortcuts import render
from django_pandas.io import read_frame
from django.db.models import Count, Q
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)

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
        },
        'defendant_stats': {
            'male': df['no_of_defendants_accused_male'].sum(),
            'female': df['no_of_defendants_accused_female'].sum(),
            'org': df['no_of_defendants_accused_organization'].sum(),
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

