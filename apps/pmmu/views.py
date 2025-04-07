# apps/pmmu/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import IndicatorNote
from apps.document_management.utils.document_manager import DocumentManager
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PMMU, PerformanceIndicator, IndicatorCategory, FinancialYearPerformance

# pmmu/views.py
@login_required
def pmmu_dashboard(request):
    """Dashboard view showing latest PMMU with categorized indicators."""
    pmmus = PMMU.objects.all().order_by('-financial_year') 
    latest_pmmu = pmmus.first()  # Get the most recent PMMU
    
    total_indicators_latest_pmmu = 0
    categories_with_indicators_data = [] # New structure to hold processed data
    categories_with_indicators_data = [] # Structure to hold processed data
    total_indicators_latest_pmmu = 0 # Initialize count

    if latest_pmmu:
        # 1. Get relevant categories for the specific financial year
        relevant_category_ids = IndicatorCategory.objects.filter(
            indicators__financial_year_data__financial_year=latest_pmmu.financial_year
        ).values_list('id', flat=True).distinct()

        # 2. Get relevant indicators within those categories for the specific financial year
        relevant_indicators_qs = PerformanceIndicator.objects.filter(
            subcategory__id__in=relevant_category_ids, # Corrected field lookup based on model definition
            financial_year_data__financial_year=latest_pmmu.financial_year
        ).distinct()

        # 3. Calculate total count from the relevant indicators
        total_indicators_latest_pmmu = relevant_indicators_qs.count()

        # 4. Pre-fetch all relevant FinancialYearPerformance data for these indicators and FY
        fy_performances = FinancialYearPerformance.objects.filter(
            financial_year=latest_pmmu.financial_year,
            indicator__in=relevant_indicators_qs # Filter by the relevant indicators QuerySet
        ).select_related('indicator') # Select related indicator

        # 5. Create a lookup dictionary: {indicator_id: fy_performance_object}
        fy_performance_lookup = {perf.indicator_id: perf for perf in fy_performances}

        # 6. Fetch categories (ordered) and structure data for the template
        categories_for_display = IndicatorCategory.objects.filter(
            pk__in=relevant_category_ids
        ).prefetch_related(
           'indicators' # Prefetch indicators again for iteration
        ).order_by('name') # Order categories

        for category in categories_for_display:
            category_data = {
                'category': category,
                'indicators': []
            }
            # Iterate through prefetched indicators for this category
            for indicator in category.indicators.all():
                # Check if this indicator has performance data for the target year using the lookup
                fy_data = fy_performance_lookup.get(indicator.id)
                if fy_data: # Only include indicators that have data for this FY
                    category_data['indicators'].append({
                        'indicator': indicator,
                        'fy_data': fy_data # Attach the specific performance data object
                    })

            # Only add category if it has relevant indicators for the year
            if category_data['indicators']:
                categories_with_indicators_data.append(category_data)

    # else: categories_with_indicators_data remains [] and total_indicators_latest_pmmu remains 0

    context = {
        'pmmus': pmmus,
        'latest_pmmu': latest_pmmu,
        'categories_data': categories_with_indicators_data, # Pass the processed data structure
        'total_indicators_latest_pmmu': total_indicators_latest_pmmu,
    }
    return render(request, 'pmmu/pmmu_dashboard.html', context)


@login_required
def add_note_document(request, note_id):
    """View to handle document attachment to notes."""
    note = get_object_or_404(IndicatorNote, pk=note_id)
    
    if request.method == 'POST' and request.FILES.get('document'):
        file = request.FILES['document']
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        
        # Use DocumentManager to attach the file
        DocumentManager.attach_document(
            file=file,
            source_object=note,
            uploaded_by=request.user,
            title=title or file.name,
            description=description,
            source_module='pmmu_app'
        )
        
        messages.success(request, 'Document attached successfully.')
        return redirect('pmmu:indicator_detail', pk=note.indicator.pk)
        
    return redirect('pmmu:indicator_detail', pk=note.indicator.pk)

@login_required
def pmmu_list(request):
    """View to list all PMMU documents."""
    pmmus = PMMU.objects.all().order_by('-financial_year', '-created_at')
    context = {'pmmus': pmmus}
    return render(request, 'pmmu/pmmu_list.html', context)

@login_required
def pmmu_detail(request, pk):
    """View to display details of a specific PMMU document."""
    pmmu = get_object_or_404(PMMU, pk=pk)
    
    # Get unique indicators for this financial year
    indicator_categories = IndicatorCategory.objects.prefetch_related(
        'indicators',
        'indicators__notes',
        'indicators__notes__created_by',
        'indicators__notes__documents',
        'indicators__financial_year_data'
    ).filter(
        indicators__financial_year_data__financial_year=pmmu.financial_year
    ).distinct()

    # Create a dictionary to store unique indicators per category
    categories_data = {}
    
    for category in indicator_categories:
        # Get unique indicators for this category
        unique_indicators = category.indicators.filter(
            financial_year_data__financial_year=pmmu.financial_year
        ).distinct()
        
        categories_data[category] = unique_indicators

    context = {
        'pmmu': pmmu,
        'categories_data': categories_data,
    }
    return render(request, 'pmmu/pmmu_detail.html', context)

    

@login_required
def indicator_list(request):
    """View to list all Performance Indicators."""
    indicators = PerformanceIndicator.objects.all().order_by('subcategory__name', 'name')
    context = {'indicators': indicators}
    return render(request, 'pmmu/indicator_list.html', context)

# views.py
@login_required
def indicator_detail(request, pk):
    """Enhanced view for individual indicator details."""
    indicator = get_object_or_404(PerformanceIndicator.objects.select_related(
        'subcategory'
    ).prefetch_related(
        'notes__created_by',
        'notes__documents',
        'financial_year_data__financial_year'
    ), pk=pk)
    
    # Get yearly performance data
    yearly_performance = indicator.financial_year_data.all().order_by('-financial_year__name')
    
    context = {
        'indicator': indicator,
        'yearly_performance': yearly_performance,
    }
    return render(request, 'pmmu/indicator_detail.html', context)


# Basic CRUD views - Create, Update, Delete (starting point - you'll need to add forms and more robust handling)

@login_required
def pmmu_create(request):
    if request.method == 'POST':
        # Form processing would go here (you need to create a PMMUForm)
        messages.success(request, "PMMU Created (Form needed)") # Placeholder
        return redirect('pmmu:pmmu_list') # Redirect to list after creation
    return render(request, 'pmmu/pmmu_form.html', {'action': 'Create'}) # Placeholder template


@login_required
def pmmu_update(request, pk):
    pmmu = get_object_or_404(PMMU, pk=pk)
    if request.method == 'POST':
        # Form processing for update (you need PMMUForm)
        messages.success(request, "PMMU Updated (Form needed)") # Placeholder
        return redirect('pmmu:pmmu_detail', pk=pk)
    return render(request, 'pmmu/pmmu_form.html', {'pmmu': pmmu, 'action': 'Update'}) # Placeholder template


@login_required
def pmmu_delete(request, pk):
    pmmu = get_object_or_404(PMMU, pk=pk)
    if request.method == 'POST':
        pmmu.delete()
        messages.success(request, "PMMU Deleted")
        return redirect('pmmu:pmmu_list')
    return render(request, 'pmmu/pmmu_confirm_delete.html', {'pmmu': pmmu})


@login_required
def add_indicator_note(request, indicator_id):
    """Add a note to an indicator using a form."""
    indicator = get_object_or_404(PerformanceIndicator, pk=indicator_id)
    
    if request.method == 'POST':
        form = IndicatorNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.indicator = indicator
            note.created_by = request.user
            note.save()
            messages.success(request, 'Note added successfully.')
        else:
            messages.error(request, 'Please correct the errors below.')
            
    return redirect('pmmu:indicator_detail', pk=indicator_id)


@login_required
def indicator_create(request, pmmu_pk): # Pass pmmu_pk to pre-select PMMU
    pmmu = get_object_or_404(PMMU, pk=pmmu_pk)
    if request.method == 'POST':
        # Form processing for Indicator (you need IndicatorForm)
        messages.success(request, "Indicator Created (Form needed)") # Placeholder
        return redirect('pmmu:pmmu_detail', pk=pmmu_pk) # Redirect back to PMMU detail
    return render(request, 'pmmu/indicator_form.html', {'pmmu': pmmu, 'action': 'Create'}) # Placeholder template


@login_required
def indicator_update(request, pk):
    indicator = get_object_or_404(PerformanceIndicator, pk=pk)
    if request.method == 'POST':
        # Form processing for Indicator update (IndicatorForm needed)
        messages.success(request, "Indicator Updated (Form needed)") # Placeholder
        return redirect('pmmu:indicator_detail', pk=pk)
    return render(request, 'pmmu/indicator_form.html', {'indicator': indicator, 'action': 'Update'}) # Placeholder template


@login_required
def indicator_delete(request, pk):
    indicator = get_object_or_404(PerformanceIndicator, pk=pk)
    pmmu_pk = indicator.subcategory.pmmu_id # Get PMMU pk to redirect back
    if request.method == 'POST':
        indicator.delete()
        messages.success(request, "Indicator Deleted")
        return redirect('pmmu:pmmu_detail', pk=pmmu_pk) # Redirect back to PMMU detail
    return render(request, 'pmmu/indicator_confirm_delete.html', {'indicator': indicator})