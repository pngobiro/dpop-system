from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from apps.statistics.models import UnitRank



def home(request):
    # show hello world string
    #  UnitRank
    context = {
        'unit_ranks': UnitRank.objects.all()
    }
    return render(request, 'statistics/home.html', context)
    

def rank_units(request, id, financial_year_id, financial_quarter_id):
    # Handle logic for rank units view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
    }
    return render(request, 'statistics/rank_units.html', context)

def rank_unit_division_months(request, id, financial_year_id, financial_quarter_id, unit_id):
    # Handle logic for rank unit months view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
    }
    return render(request, 'statistics/rank_unit_months.html', context)

def rank_unit_month(request, id, financial_year_id, financial_quarter_id, unit_id, month_id):
    # Handle logic for rank unit month view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/rank_unit_month.html', context)

def rank_unit_division_month_cases_summary(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for rank unit division month cases summary view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/rank_unit_division_month_cases_summary.html', context)

def upload_unit_monthly_dcrt_excel(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for upload unit monthly dcrt excel view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/upload_unit_monthly_dcrt_excel.html', context)

def save_unit_monthly_dcrt_excel(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for save unit monthly dcrt excel view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/save_unit_monthly_dcrt_excel.html', context)


def remove_missing_values(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for remove missing values view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/remove_missing_values.html', context)


def remove_outliers(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for remove outliers view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/remove_outliers.html', context)


def view_missing_values(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for view missing values view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/view_missing_values.html', context)


def view_outliers(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for view outliers view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/view_outliers.html', context)


