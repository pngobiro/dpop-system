from django.shortcuts import render, HttpResponse, redirect
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, Months
)
from apps.statistics.utils.file_upload import handle_uploaded_file

def upload_unit_monthly_dcrt_excel(request, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    """Handle Excel file upload for monthly DCRT data."""
    
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