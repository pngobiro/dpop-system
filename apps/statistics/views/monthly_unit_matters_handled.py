from django.shortcuts import render, HttpResponse
from django_pandas.io import read_frame
import pandas as pd
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)

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