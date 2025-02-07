      
# apps/mail/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Avg, F  # Import Avg and F
from django.utils import timezone
from django.http import HttpResponseNotFound  # Import for 404
from .models import PhysicalMail, MailActivity, MailMovement, generate_tracking_number
from .forms import (
    PhysicalMailForm, MailReceiptForm, MailDispatchForm,
    MailMovementForm
)

@login_required
def mail_dashboard(request):
    """Main dashboard for physical mail handling"""
    today = timezone.now().date()
    department = request.user.department

    # Get statistics
    stats = {
        'total_mail': PhysicalMail.objects.filter(department=department).count(),
        'pending_receipt': PhysicalMail.objects.filter(
            department=department,
            status='received'
        ).count(),
        'in_transit': PhysicalMail.objects.filter(
            department=department,
            status='in_transit'
        ).count(),
        'dispatched_today': PhysicalMail.objects.filter(
            department=department,
            status='dispatched',
            date_sent__date=today
        ).count()
    }

    # Recent activities
    recent_activities = MailActivity.objects.filter(
        mail__department=department
    ).select_related('mail', 'user').order_by('-timestamp')[:10]

    # Pending mail
    pending_mail = PhysicalMail.objects.filter(
        department=department,
        status__in=['received', 'pending_dispatch']
    ).order_by('-created_at')[:5]

    context = {
        'stats': stats,
        'recent_activities': recent_activities,
        'pending_mail': pending_mail
    }
    return render(request, 'mail/dashboard.html', context)

@login_required
def register_mail(request):
    """Register new physical mail"""
    if request.method == 'POST':
        form = PhysicalMailForm(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.created_by = request.user
            mail.department = request.user.department
            # mail.tracking_number = generate_tracking_number() # No longer need as moved to signals
            mail.save()

            # Record activity - Now in signals
            # MailActivity.objects.create(
            #     mail=mail,
            #     user=request.user,
            #     action='register',
            #     location=request.user.department.name
            # )

            messages.success(request, 'Mail registered successfully.')
            return redirect('mail:mail_detail', pk=mail.pk)  # Correct redirect
    else:
        form = PhysicalMailForm()

    return render(request, 'mail/register_mail.html', {'form': form})



@login_required
def mail_detail(request, pk):
    """View details of a specific mail item."""
    try:
        mail = PhysicalMail.objects.get(pk=pk)
    except PhysicalMail.DoesNotExist:
        return HttpResponseNotFound("Mail item not found.")  # Use HttpResponseNotFound

    # Check if the user has permission to view this mail
    if mail.department != request.user.department and not request.user.has_perm('mail.view_confidential_mail'):
        messages.error(request, "You do not have permission to view this mail item.")
        return redirect('mail:mail_dashboard')  # Or another appropriate view

    activities = MailActivity.objects.filter(mail=mail).order_by('-timestamp')
    movements = MailMovement.objects.filter(mail=mail).order_by('-timestamp')
    # Add other related data as needed (e.g., attachments)

    context = {
        'mail': mail,
        'activities': activities,
        'movements': movements,
        # Add other context variables here
    }
    return render(request, 'mail/mail_detail.html', context)
@login_required
def record_mail_movement(request, pk):
    """Record movement of physical mail"""
    mail = get_object_or_404(PhysicalMail, pk=pk)

    if request.method == 'POST':
        form = MailMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.mail = mail
            movement.handler = request.user
            movement.save()

            # Update mail status
            mail.status = 'in_transit'
            mail.save()

            # Record activity
            MailActivity.objects.create(
                mail=mail,
                user=request.user,
                action='forward',
                location=movement.to_location
            )

            messages.success(request, 'Mail movement recorded successfully.')
            return redirect('mail:mail_detail', pk=mail.pk)
    else:
        form = MailMovementForm()

    context = {
        'form': form,
        'mail': mail
    }
    return render(request, 'mail/record_movement.html', context)

@login_required
def mail_movement_report(request):
    """Generate report for mail movement"""
    department = request.user.department

    # Filter parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status = request.GET.get('status')

    movements = MailMovement.objects.filter(
        mail__department=department
    ).select_related('mail', 'handler')

    if date_from:
        movements = movements.filter(timestamp__date__gte=date_from)
    if date_to:
        movements = movements.filter(timestamp__date__lte=date_to)
    if status:
        movements = movements.filter(mail__status=status)

    # Summary statistics  CORRECTED HERE
    summary = {
        'total_movements': movements.count(),
        'avg_delivery_time': movements.aggregate(avg_delivery_time=Avg(F('received_at') - F('mail__date_sent'))),
        'by_status': movements.values('mail__status').annotate(
            count=Count('id')
        )
    }

    context = {
        'movements': movements,
        'summary': summary,
        'date_from': date_from,
        'date_to': date_to,
        'status': status
    }
    return render(request, 'mail/movement_report.html', context)

@login_required
def dispatch_mail(request, pk):
    """Dispatch physical mail"""
    mail = get_object_or_404(PhysicalMail, pk=pk)

    if request.method == 'POST':
        form = MailDispatchForm(request.POST)
        if form.is_valid():
            # Update mail details
            mail.status = 'dispatched'
            mail.date_sent = form.cleaned_data['dispatch_date']
            mail.delivery_method = form.cleaned_data['delivery_method']
            mail.courier_name = form.cleaned_data['courier_name']
            mail.courier_tracking_number = form.cleaned_data['tracking_number']
            mail.save()

            # Record activity
            MailActivity.objects.create(
                mail=mail,
                user=request.user,
                action='dispatch',
                notes=form.cleaned_data['notes']
            )

            messages.success(request, 'Mail dispatched successfully.')
            return redirect('mail:mail_detail', pk=mail.pk)
    else:
        form = MailDispatchForm()

    context = {
        'form': form,
        'mail': mail
    }
    return render(request, 'mail/dispatch_mail.html', context)

