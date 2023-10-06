from django.shortcuts import render



def home(request):
    # Handle logic for dashboard view here
    return render(request, 'statistics/dashboard.html')
    

def rank(request, id, financial_year_id, financial_quarter_id):
    # Handle logic for rank view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
    }
    return render(request, 'statistics/rank.html', context)

def rank_units(request, id, financial_year_id, financial_quarter_id):
    # Handle logic for rank units view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
    }
    return render(request, 'statistics/rank_units.html', context)

def rank_unit_months(request, id, financial_year_id, financial_quarter_id, unit_id):
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
