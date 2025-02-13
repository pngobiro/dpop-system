# apps/pmmu/views.py
from django.shortcuts import render, get_object_or_404, redirect
from apps.pmmu.models import Indicator, IndicatorNote, PMMU # Updated import
from .forms import IndicatorNoteForm

def pmmu_dashboard(request):
    """Display the PMMU Dashboard"""
    pmmus = PMMU.objects.all() # Get PMMUs instead of Indicators
    context = {
        'pmmus': pmmus, # Pass PMMUs to the template
    }
    return render(request, 'pmmu/pmmu_dashboard.html', context)


def pmmu_item_detail(request, pk):
    """Display details for a specific PMMU, including Indicators and a form to add new Indicators"""
    pmmu = get_object_or_404(PMMU, pk=pk)
    indicator_form = IndicatorForm()

    if request.method == 'POST':
        indicator_form = IndicatorForm(request.POST)
        if indicator_form.is_valid():
            indicator = indicator_form.save(commit=False)
            indicator.pmmu = pmmu
            indicator.created_by = request.user
            indicator.save()
            return redirect('pmmu:pmmu_item_detail', pk=pk)

    context = {
        'pmmu': pmmu,
        'indicator_form': indicator_form,
    }
    return render(request, 'pmmu/pmmu_item_detail.html', context)

def pmmu_item_list(request, pmmu_pk): # Pass pmmu_pk to filter indicators
    """Display a list of Indicators for a specific PMMU"""
    pmmu = get_object_or_404(PMMU, pk=pmmu_pk) # Get the PMMU
    indicators = Indicator.objects.filter(pmmu=pmmu) # Filter indicators by PMMU
    context = {
        'pmmu': pmmu, # Pass PMMU to template for context
        'indicators': indicators,
    }
    return render(request, 'pmmu/pmmu_item_list.html', context)

def pmmu_item_detail(request, pk):
    """Display details for a specific Indicator, including notes and a form to add new notes"""
    indicator = get_object_or_404(Indicator, pk=pk)
    note_form = IndicatorNoteForm()

    if request.method == 'POST':
        note_form = IndicatorNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.indicator = indicator
            note.created_by = request.user
            note.save()
            return redirect('pmmu:pmmu_item_detail', pk=pk)

    context = {
        'indicator': indicator,
        'note_form': note_form,
    }
    return render(request, 'pmmu/pmmu_item_detail.html', context)


def indicator_detail(request, pk):
    """Display details for a specific Indicator, including notes and a form to add new notes"""
    indicator = get_object_or_404(Indicator, pk=pk)
    note_form = IndicatorNoteForm()

    if request.method == 'POST':
        note_form = IndicatorNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.indicator = indicator
            note.created_by = request.user
            note.save()
            return redirect('pmmu:indicator_detail', pk=pk) # Redirect to indicator_detail view after adding note

    context = {
        'indicator': indicator,
        'note_form': note_form,
    }
    return render(request, 'pmmu/pmmu_item_detail.html', context) # Template name remains pmmu_item_detail for now, we'll rename later if needed


# indicator_list view

def indicator_list(request, pmmu_pk):
    """Display a list of Indicators for a specific PMMU"""
    pmmu = get_object_or_404(PMMU, pk=pmmu_pk)
    indicators = Indicator.objects.filter(pmmu=pmmu)
    context = {
        'pmmu': pmmu,
        'indicators': indicators,
    }
    return render(request, 'pmmu/indicator_list.html', context)