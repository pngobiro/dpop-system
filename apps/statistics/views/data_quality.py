# apps/statistics/views/data_quality.py

from django.shortcuts import render, HttpResponse
from django_pandas.io import read_frame
import pandas as pd
from django.db.models import Count, Q
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, DcrtData, Months
)

def monthly_unit_outliers(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """Analyze and display statistical outliers in the data."""
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

        df = read_frame(queryset)
        
        # Define numerical columns to check for outliers
        numeric_columns = [
            'no_of_plaintiffs_or_appellants_male',
            'no_of_plaintiffs_or_appellants_female',
            'no_of_plaintiffs_or_appellants_organization',
            'no_of_defendants_accused_male',
            'no_of_defendants_accused_female',
            'no_of_defendants_accused_organization',
            'no_of_witnesses_in_court_d',
            'no_of_witnesses_in_court_w',
            'no_of_accused_remanded'
        ]

        outliers = {}
        for column in numeric_columns:
            if column in df.columns:
                # Calculate Q1, Q3, and IQR
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                
                # Define outlier bounds
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Find outliers
                outliers[column] = {
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'outliers': df[
                        (df[column] < lower_bound) | 
                        (df[column] > upper_bound)
                    ][['case_number_code', column]].to_dict('records'),
                    'count': len(df[
                        (df[column] < lower_bound) | 
                        (df[column] > upper_bound)
                    ])
                }

        context = {
            'unit_rank': unit_rank,
            'financial_year': fy,
            'financial_quarter': fq,
            'unit': unit,
            'division': division,
            'month': month,
            'outliers': outliers,
            'total_records': len(df)
        }
        
        return render(request, 'statistics/monthly_unit_outliers.html', context)
        
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def monthly_unit_missing_data(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """Analyze and display missing data patterns."""
    try:
        # Get base objects and data
        unit_rank = UnitRank.objects.get(id=id)
        fy = FinancialYear.objects.get(id=financial_year_id)
        fq = FinancialQuarter.objects.get(id=financial_quarter_id)
        unit = Unit.objects.get(id=unit_id)
        division = Division.objects.get(id=division_id)
        month = Months.objects.get(id=month_id)

        queryset = DcrtData.objects.filter(
            financial_year=financial_year_id,
            financial_quarter=financial_quarter_id,
            unit=unit_id,
            division=division_id,
            month=month_id
        )

        df = read_frame(queryset)
        
        # Calculate missing values for each column
        missing_data = {
            column: {
                'missing_count': df[column].isna().sum(),
                'missing_percentage': round(df[column].isna().sum() / len(df) * 100, 2),
                'examples': df[df[column].isna()]['case_number_code'].tolist()[:5]
            }
            for column in df.columns
            if df[column].isna().sum() > 0
        }

        context = {
            'unit_rank': unit_rank,
            'financial_year': fy,
            'financial_quarter': fq,
            'unit': unit,
            'division': division,
            'month': month,
            'missing_data': missing_data,
            'total_records': len(df)
        }
        
        return render(request, 'statistics/monthly_unit_missing_data.html', context)
        
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def monthly_unit_duplicate_data(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """Identify and display duplicate records."""
    try:
        # Get base objects and data
        unit_rank = UnitRank.objects.get(id=id)
        fy = FinancialYear.objects.get(id=financial_year_id)
        fq = FinancialQuarter.objects.get(id=financial_quarter_id)
        unit = Unit.objects.get(id=unit_id)
        division = Division.objects.get(id=division_id)
        month = Months.objects.get(id=month_id)

        queryset = DcrtData.objects.filter(
            financial_year=financial_year_id,
            financial_quarter=financial_quarter_id,
            unit=unit_id,
            division=division_id,
            month=month_id
        )

        df = read_frame(queryset)
        
        # Find duplicates based on case number
        duplicates = df[df.duplicated(subset=['case_number_code', 'case_number_number'], keep=False)]
        
        context = {
            'unit_rank': unit_rank,
            'financial_year': fy,
            'financial_quarter': fq,
            'unit': unit,
            'division': division,
            'month': month,
            'duplicate_count': len(duplicates),
            'duplicate_cases': duplicates.to_dict('records'),
            'total_records': len(df)
        }
        
        return render(request, 'statistics/monthly_unit_duplicate_data.html', context)
        
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def monthly_unit_incomplete_data(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """Analyze and display incomplete records."""
    try:
        # Get base objects and data
        unit_rank = UnitRank.objects.get(id=id)
        fy = FinancialYear.objects.get(id=financial_year_id)
        fq = FinancialQuarter.objects.get(id=financial_quarter_id)
        unit = Unit.objects.get(id=unit_id)
        division = Division.objects.get(id=division_id)
        month = Months.objects.get(id=month_id)

        queryset = DcrtData.objects.filter(
            financial_year=financial_year_id,
            financial_quarter=financial_quarter_id,
            unit=unit_id,
            division=division_id,
            month=month_id
        )

        df = read_frame(queryset)
        
        # Define required fields
        required_fields = [
            'case_number_code',
            'case_number_number',
            'specific_case_type',
            'case_outcome'
        ]
        
        # Find incomplete records
        incomplete_records = df[df[required_fields].isna().any(axis=1)]
        
        context = {
            'unit_rank': unit_rank,
            'financial_year': fy,
            'financial_quarter': fq,
            'unit': unit,
            'division': division,
            'month': month,
            'incomplete_count': len(incomplete_records),
            'incomplete_cases': incomplete_records.to_dict('records'),
            'total_records': len(df),
            'required_fields': required_fields
        }
        
        return render(request, 'statistics/monthly_unit_incomplete_data.html', context)
        
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
    