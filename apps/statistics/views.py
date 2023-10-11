from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django_pandas.io import read_frame
import urllib.request
from .utils import handle_uploaded_file
from apps.statistics.models import UnitRank , FinancialYear , FinancialQuarter , Unit , Months , DcrtData , Division



def home(request):
    # show hello world string
    #  UnitRank
    context = {
        'unit_ranks': UnitRank.objects.all(),
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
    }
    return render(request, 'statistics/home.html', context)
    

def rank_units(request, id, financial_year_id, financial_quarter_id):
    # Handle logic for rank units view here

    #  UnitRank

    unit_rank = UnitRank.objects.get(id=id)

    fy = FinancialYear.objects.get(id=financial_year_id)

    fq = FinancialQuarter.objects.get(id=financial_quarter_id)



    context = {
        'units': Unit.objects.filter(unit_rank=id),
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
    }
    return render(request, 'statistics/rank_units.html', context)

def rank_unit_division_months(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    # Handle logic for rank unit months view here

    #  UnitRank
    unit_rank = UnitRank.objects.get(id=id)

    fy = FinancialYear.objects.get(id=financial_year_id)

    fq = FinancialQuarter.objects.get(id=financial_quarter_id)

    unit = Unit.objects.get(id=unit_id)

    division = Division.objects.get(id=25)
     
    context = {
        'months': Months.objects.filter(financial_quarter=fq.quarter_number),
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        }
      
    return render(request, 'statistics/rank_unit_months.html', context)

def rank_unit_month(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    #  months dictionary with e.g id 1 as key and January as value
    unit_rank = UnitRank.objects.get(id=id)

    fy = FinancialYear.objects.get(id=financial_year_id)

    fq = FinancialQuarter.objects.get(id=financial_quarter_id)

    unit = Unit.objects.get(id=unit_id)

    division = Division.objects.get(id=25)

    month = Months.objects.get(id=month_id)


  

    context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,
    }
    return render(request, 'statistics/rank_unit_month.html', context)

def rank_unit_division_month_cases_summary(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    #  unit_rank = UnitRank.objects.get(id=id)
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=25)
    month = Months.objects.get(id=month_id)

    context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,
    }
    return render(request, 'statistics/rank_unit_division_month_cases_summary.html', context)

def upload_unit_monthly_dcrt_excel(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for upload unit monthly dcrt excel view here

    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=25)
    month = Months.objects.get(id=month_id)


    if request.method == 'POST':
        excel_file = request.FILES.get("excelFile")  # Get the uploaded file

        if excel_file:
            handle_uploaded_file(excel_file, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id)  # Call the function to handle the uploaded file
            # go to statistics:case_summary path
            return HttpResponseRedirect('/statistics/rank/' + str(id) + '/fy/' + str(financial_year_id) + '/fq/' + str(financial_quarter_id) + '/units/' + str(unit_id) + '/division/' + str(division_id) + '/months/' + str(month_id) + '/cases/case_summary')
           
        else:
            return HttpResponse("No file uploaded.")
    
    else:

        context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,
    }
        
        return render(request, 'statistics/upload_unit_monthly_dcrt_excel.html', context)
    
def case_summary(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    unit_rank = UnitRank.objects.get(id=id)
    fy = FinancialYear.objects.get(id=financial_year_id)
    fq = FinancialQuarter.objects.get(id=financial_quarter_id)
    unit = Unit.objects.get(id=unit_id)
    division = Division.objects.get(id=25)
    month = Months.objects.get(id=month_id)
    queryset = DcrtData.objects.filter(financial_year=financial_year_id, financial_quarter=financial_quarter_id, unit=unit_id, division=division_id, month=month_id)

    context = {
        'unit_rank': unit_rank,
        'financial_year': fy,
        'financial_quarter': fq,
        'unit': unit,
        'division': division,
        'month': month,
    }
    return render(request, 'statistics/case_summary.html', context)





def monthly_unit_outliers(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for remove missing values view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/monthly_unit_outliers.html', context)


def monthly_unit_missing_data(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for remove outliers view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/monthly_unit_missing_data.html', context)


def monthly_unit_registered_cases(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    queryset = DcrtData.objects.all()
    df = read_frame(queryset)
     # count of registered cases . look for case_outcome with phrase 'Case Registered/Filed' . count them, skip null values

    registered_cases = df[df['case_outcome'].str.contains('Case Registered/Filed', na=False)].shape[0]

    # registered_cases by case_number_code and count each case_number_code

    registered_cases_group = df.groupby('case_number_code').count()

    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
        'registered_cases': registered_cases,
        'registered_cases_group': registered_cases_group,
    }
    return render(request, 'statistics/monthly_unit_registered_cases.html', context)


# monthly_unit_duplicate_data

def monthly_unit_duplicate_data(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    

    queryset = DcrtData.objects.all()
    df = read_frame(queryset)
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
        'duplicate_cases': duplicate_cases,
        'duplicate_cases_group': duplicate_cases_group,
    }

    return render(request, 'statistics/monthly_unit_duplicate_data.html', context)




def monthly_unit_resolved_cases(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Handle logic for view outliers view here
    context = {
        'id': id,
        'financial_year_id': financial_year_id,
        'financial_quarter_id': financial_quarter_id,
        'unit_id': unit_id,
        'division_id': division_id,
        'month_id': month_id,
    }
    return render(request, 'statistics/monthly_unit_resolved_cases.html', context)


# unit_division_quarters

def unit_division_quarters(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    # Handle logic for unit division quarters view here
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
        'division_id': division_id,
    }
    return render(request, 'statistics/unit_division_quarters.html', context)


# monthly_unit_matters_handled

def monthly_unit_matters_handled(request, id, financial_year_id, financial_quarter_id, unit_id , division_id , month_id):
    # Handle logic for monthly unit matters handled view here
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
    }
    return render(request, 'statistics/monthly_unit_matters_handled.html', context)

# monthly_unit_incomplete_data

def monthly_unit_incomplete_data(request, id, financial_year_id, financial_quarter_id, unit_id , division_id , month_id):
    # Handle logic for monthly unit incomplete data view here
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
    }
    return render(request, 'statistics/monthly_unit_incomplete_data.html', context)


# unit_division_fy

def unit_division_fy(request, id, financial_year_id, financial_quarter_id, unit_id , division_id):
    # Handle logic for unit division fy view here
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
    }
    return render(request, 'statistics/unit_division_fy.html', context)


# monthly_unit_duplicate_data

def monthly_unit_duplicate_data(request, id, financial_year_id, financial_quarter_id, unit_id , division_id , month_id):
    # Handle logic for monthly unit duplicate data view here
    context = {
        'financial_years': FinancialYear.objects.all(),
        'financial_quarters': FinancialQuarter.objects.all(),
        'id': id,
        'unit_id': unit_id,
    }
    return render(request, 'statistics/monthly_unit_duplicate_data.html', context)

