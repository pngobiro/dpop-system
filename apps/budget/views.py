# apps/budget/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import WorkplanItem, QuarterlyAllocation, FinancialYear

@login_required
def workplan_summary(request):
    """Display overall workplan summary"""
    current_fy = FinancialYear.objects.first()  # Get current financial year
    workplan_items = WorkplanItem.objects.filter(financial_year=current_fy)
    
    # Calculate totals by quarter
    quarterly_totals = {
        1: QuarterlyAllocation.objects.filter(workplan_item__financial_year=current_fy, quarter=1).aggregate(Sum('amount'))['amount__sum'] or 0,
        2: QuarterlyAllocation.objects.filter(workplan_item__financial_year=current_fy, quarter=2).aggregate(Sum('amount'))['amount__sum'] or 0,
        3: QuarterlyAllocation.objects.filter(workplan_item__financial_year=current_fy, quarter=3).aggregate(Sum('amount'))['amount__sum'] or 0,
        4: QuarterlyAllocation.objects.filter(workplan_item__financial_year=current_fy, quarter=4).aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    
    total_budget = sum(quarterly_totals.values())
    
    # Get items with their quarterly allocations
    items_with_quarters = []
    for item in workplan_items:
        quarterly_data = {
            allocation.quarter: allocation.amount 
            for allocation in item.quarterlyallocation_set.all()
        }
        items_with_quarters.append({
            'item': item,
            'q1_amount': quarterly_data.get(1, 0),
            'q2_amount': quarterly_data.get(2, 0),
            'q3_amount': quarterly_data.get(3, 0),
            'q4_amount': quarterly_data.get(4, 0),
            'total': item.total_amount,
            'indicators': item.performanceindicator_set.all()
        })

    context = {
        'financial_year': current_fy,
        'items': items_with_quarters,
        'quarterly_totals': quarterly_totals,
        'total_budget': total_budget
    }
    return render(request, 'budget/workplan_summary.html', context)

@login_required
def transformative_initiatives(request):
    """Display transformative initiatives"""
    initiatives = WorkplanItem.objects.filter(
        item_type='transformative'
    ).select_related('transformativeinitiative')
    
    context = {
        'initiatives': initiatives
    }
    return render(request, 'budget/transformative_initiatives.html', context)

@login_required
def performance_indicators(request):
    """Display performance indicators"""
    workplan_items = WorkplanItem.objects.prefetch_related('performanceindicator_set')
    
    context = {
        'workplan_items': workplan_items
    }
    return render(request, 'budget/performance_indicators.html', context)