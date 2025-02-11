
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Count  # Import Count
from apps.statistics.models import FinancialYear  # Import FinancialYear
from .forms import InnovationForm, InnovationAttachmentFormSet
from .models import Innovation, InnovationAttachment
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import the messages framework
from django.utils import timezone #import timezone
from django.http import HttpResponseForbidden, HttpResponse



@login_required
@permission_required('innovations.view_innovation', raise_exception=True) #add permissions
def dashboard(request):
    # Get the selected financial year from the request, or default to the current year
    current_fy = FinancialYear.objects.order_by('-start_date').first()  # Get *latest* FY
    selected_fy_id = request.GET.get('financial_year', current_fy.pk if current_fy else None) # None if no FY at all

    try:
        selected_fy = FinancialYear.objects.get(pk=selected_fy_id)
    except FinancialYear.DoesNotExist:
        selected_fy = current_fy  # Fallback to current, or could return a 404/error
    
    # Base query, filtered by user permissions
    if request.user.is_superuser:
        base_query = Q(financial_year=selected_fy)
    else:
       base_query = Q(financial_year=selected_fy) & (Q(submitted_by=request.user) | Q(court__in=request.user.departments.all())) # Use court, not department

    # Calculate statistics
    stats = {
        'total': Innovation.objects.filter(base_query).count(),
        'innovations': Innovation.objects.filter(base_query, status='innovation').count(),
        'best_practices': Innovation.objects.filter(base_query, status='best_practice').count(),
        'rejected': Innovation.objects.filter(base_query, status='rejected').count(),
    }

    # Get recent innovations (limit to, say, the last 5)
    recent_innovations = Innovation.objects.filter(base_query).order_by('-submitted_at')[:5]


    financial_years = FinancialYear.objects.all()  # Get all financial years for the dropdown

    context = {
        'stats': stats,
        'recent_innovations': recent_innovations,
        'financial_years': financial_years,
        'selected_fy': selected_fy,  # Pass the *selected* financial year object
    }
    return render(request, 'innovations/dashboard.html', context)


@login_required
def submit_innovation(request):
    if request.method == 'POST':
        form = InnovationForm(request.POST)
        formset = InnovationAttachmentFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            innovation = form.save(commit=False)
            innovation.submitted_by = request.user
            innovation.save()

            for form in formset:
                if form.cleaned_data:  # Avoid processing empty forms
                  attachment = form.save(commit=False)
                  attachment.innovation = innovation
                  attachment.uploaded_by = request.user
                  attachment.save()

            messages.success(request, 'Innovation submitted successfully!')  # Success message
            return redirect('innovations:innovation_list')  # Redirect after successful submission

        else: # Display form errors with Bootstrap formatting
          for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label}: {error}")

          for error in formset.non_form_errors():
            messages.error(request, error)

    else:
        form = InnovationForm()
        formset = InnovationAttachmentFormSet(queryset=InnovationAttachment.objects.none())  # Empty initial formset

    return render(request, 'innovations/submit_innovation.html', {'form': form, 'formset': formset})



@login_required
@permission_required('innovations.can_view_innovation', raise_exception=True)
def innovation_list(request):
    # Filter innovations based on user's permissions and department
    if request.user.is_superuser:
        innovations = Innovation.objects.all()  # Superuser can see all
    else:
       # User sees their submissions and department innovations
        innovations = Innovation.objects.filter(
        Q(submitted_by=request.user) | Q(court__in=request.user.departments.all())
         ).distinct()

    return render(request, 'innovations/innovation_list.html', {'innovations': innovations})


@login_required
def innovation_detail(request, pk):
    innovation = get_object_or_404(Innovation, pk=pk)
    # Check permissions
    if not request.user.is_superuser and request.user != innovation.submitted_by and request.user.department != innovation.court.department: #changed to court as it is now a foreign key

        return HttpResponseForbidden("You don't have permission to view this innovation.") # used HttpResponseForbidden

    return render(request, 'innovations/innovation_detail.html', {'innovation': innovation})



@login_required
def approve_innovation(request, pk):
    innovation = get_object_or_404(Innovation, pk=pk)
    # Check permission to approve. Use the new helper function
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can approve.")

    if request.method == 'POST':
        innovation.status = 'best_practice'  # Approve
        innovation.approved_by = request.user
        innovation.approved_at = timezone.now() # use timezone.now()
        innovation.save()
        messages.success(request, 'Innovation approved!')  # Provide feedback
        return redirect('innovations:innovation_list')

    return render(request, 'innovations/approve_innovation.html', {'innovation': innovation})


@login_required
def reject_innovation(request, pk):
    innovation = get_object_or_404(Innovation, pk=pk)

    # Check permission to reject. Only admins can reject:
    if not request.user.is_superuser:
      return HttpResponseForbidden("Only admins can reject.")


    if request.method == 'POST':
        innovation.status = 'rejected'
        innovation.save()
        messages.success(request, 'Innovation rejected.')
        return redirect('innovations:innovation_list')  # Redirect after rejection
    return render(request, 'innovations/reject_innovation.html', {'innovation': innovation})



@login_required
@permission_required('innovations.can_change_innovation', raise_exception=True)
def edit_innovation(request, pk):
    innovation = get_object_or_404(Innovation, pk=pk)

    # Check if the user has permission to edit
    if request.user != innovation.submitted_by and not request.user.is_superuser:
      return HttpResponseForbidden("You do not have permission to edit this innovation.")


    if request.method == 'POST':
        form = InnovationForm(request.POST, instance=innovation)
        formset = InnovationAttachmentFormSet(request.POST, request.FILES, instance=innovation)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Innovation updated successfully!')
            return redirect('innovations:innovation_detail', pk=innovation.pk)
        else: #added form errors to template
          for field, errors in form.errors.items():
              for error in errors:
                  messages.error(request, f"{form.fields[field].label}: {error}")
          for error in formset.non_form_errors():
            messages.error(request, error)
    else:
        form = InnovationForm(instance=innovation)
        formset = InnovationAttachmentFormSet(instance=innovation)

    return render(request, 'innovations/edit_innovation.html', {'form': form, 'formset': formset, 'innovation': innovation})


@login_required
def delete_innovation(request, pk):
    innovation = get_object_or_404(Innovation, pk=pk)

    #check permission
    if request.user != innovation.submitted_by and not request.user.is_superuser: # added superuser
        return HttpResponseForbidden("You do not have permission to delete this innovation.")


    if request.method == 'POST':
        innovation.delete()
        messages.success(request, 'Innovation deleted successfully!') # added form errors
        return redirect('innovations:innovation_list')

    return render(request, 'innovations/innovation_confirm_delete.html', {'innovation': innovation})


@login_required
def download_attachment(request, attachment_id):
    attachment = get_object_or_404(InnovationAttachment, pk=attachment_id)

    # Check if user has permission to download:
    if not request.user.is_superuser and request.user != attachment.innovation.submitted_by and request.user.department != attachment.innovation.court.department: # use court instead of department
        return HttpResponseForbidden("You don't have permission to download this file.")

    # Serve the file using Django's built-in static files handling:
    response = HttpResponse(attachment.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{attachment.file.name}"'
    return response