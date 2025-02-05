# apps/meetings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Meeting, MeetingParticipant, MeetingDocument, MeetingAction
from .forms import MeetingForm, MeetingDocumentForm, MeetingActionForm
from apps.organization.models import Department
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


@login_required
def meetings_dashboard(request):
    """Dashboard view for meetings overview"""
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get counts for different meeting statuses
    upcoming_meetings = Meeting.objects.filter(
        date__gte=today,
        status='scheduled'
    ).order_by('date', 'start_time')[:5]
    
    recent_meetings = Meeting.objects.filter(
        date__lt=today
    ).order_by('-date', '-start_time')[:5]
    
    # Meeting statistics
    stats = {
        'total_meetings': Meeting.objects.filter(date__gte=thirty_days_ago).count(),
        'upcoming_count': Meeting.objects.filter(date__gte=today, status='scheduled').count(),
        'completed_count': Meeting.objects.filter(status='completed', date__gte=thirty_days_ago).count(),
        'cancelled_count': Meeting.objects.filter(status='cancelled', date__gte=thirty_days_ago).count(),
    }
    
    # Meetings by type
    meetings_by_type = Meeting.objects.filter(
        date__gte=thirty_days_ago
    ).values('meeting_type').annotate(
        count=Count('id')
    )
    
    # Meetings by mode
    meetings_by_mode = Meeting.objects.filter(
        date__gte=thirty_days_ago
    ).values('meeting_mode').annotate(
        count=Count('id')
    )
    
    # My meetings (where user is organizer or participant)
    my_meetings = Meeting.objects.filter(
        Q(organizer=request.user) | Q(participants=request.user),
        date__gte=today
    ).distinct().order_by('date', 'start_time')[:5]

    context = {
        'stats': stats,
        'upcoming_meetings': upcoming_meetings,
        'recent_meetings': recent_meetings,
        'my_meetings': my_meetings,
        'meetings_by_type': meetings_by_type,
        'meetings_by_mode': meetings_by_mode,
    }
    
    return render(request, 'meetings/dashboard.html', context)


@login_required
def meeting_list(request):
    """View for listing meetings based on user's role and department"""
    user = request.user
    
    # Check if user is director or has permission to view all meetings
    is_director = user.has_perm('meetings.view_all_meetings')
    
    if is_director:
        meetings = Meeting.objects.all()
    else:
        # Get meetings where user is organizer or participant
        meetings = Meeting.objects.filter(
            Q(department=user.department) |
            Q(participants=user)
        ).distinct()
    
    # Filter options
    status = request.GET.get('status')
    meeting_type = request.GET.get('meeting_type')
    department_id = request.GET.get('department')
    
    if status:
        meetings = meetings.filter(status=status)
    if meeting_type:
        meetings = meetings.filter(meeting_type=meeting_type)
    if department_id and is_director:
        meetings = meetings.filter(department_id=department_id)
    
    # Pagination
    paginator = Paginator(meetings, 10)
    page = request.GET.get('page')
    meetings = paginator.get_page(page)
    
    context = {
        'meetings': meetings,
        'departments': Department.objects.all() if is_director else None,
        'is_director': is_director,
    }
    
    return render(request, 'meetings/meeting_list.html', context)

@login_required
def meeting_detail(request, pk):
    """View for meeting details"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user
    
    # Check permissions
    if not (user.has_perm('meetings.view_all_meetings') or
            user.department == meeting.department or
            meeting.participants.filter(id=user.id).exists()):
        messages.error(request, "You don't have permission to view this meeting.")
        return redirect('meeting_list')
    
    context = {
        'meeting': meeting,
        'participants': MeetingParticipant.objects.filter(meeting=meeting),
        'documents': MeetingDocument.objects.filter(meeting=meeting),
        'actions': MeetingAction.objects.filter(meeting=meeting),
        'can_edit': user.has_perm('meetings.change_meeting') or meeting.organizer == user,
    }
    
    return render(request, 'meetings/meeting_detail.html', context)

@login_required
def meeting_create(request):
    """View for creating a new meeting"""
    if not request.user.has_perm('meetings.add_meeting'):
        messages.error(request, "You don't have permission to create meetings.")
        return redirect('meeting_list')
    
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.organizer = request.user
            meeting.save()
            form.save_m2m()  # Save participants
            
            # Create participant entries
            for user in form.cleaned_data['participants']:
                MeetingParticipant.objects.create(
                    meeting=meeting,
                    participant=user
                )
            
            messages.success(request, 'Meeting created successfully.')
            return redirect('meeting_detail', pk=meeting.pk)
    else:
        form = MeetingForm()
        
    return render(request, 'meetings/meeting_form.html', {'form': form, 'action': 'Create'})

@login_required
def meeting_update(request, pk):
    """View for updating an existing meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    
    if not (request.user.has_perm('meetings.change_meeting') or meeting.organizer == request.user):
        messages.error(request, "You don't have permission to edit this meeting.")
        return redirect('meeting_detail', pk=pk)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            messages.success(request, 'Meeting updated successfully.')
            return redirect('meeting_detail', pk=meeting.pk)
    else:
        form = MeetingForm(instance=meeting)
        
    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'meeting': meeting,
        'action': 'Update'
    })

@login_required
def meeting_delete(request, pk):
    """View for deleting a meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    
    if not (request.user.has_perm('meetings.delete_meeting') or meeting.organizer == request.user):
        messages.error(request, "You don't have permission to delete this meeting.")
        return redirect('meeting_detail', pk=pk)
    
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted successfully.')
        return redirect('meeting_list')
        
    return render(request, 'meetings/meeting_confirm_delete.html', {'meeting': meeting})

@login_required
def meeting_document_upload(request, meeting_pk):
    """View for uploading meeting documents"""
    meeting = get_object_or_404(Meeting, pk=meeting_pk)
    
    if request.method == 'POST':
        form = MeetingDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.meeting = meeting
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('meeting_detail', pk=meeting_pk)
    else:
        form = MeetingDocumentForm()
        
    return render(request, 'meetings/document_upload.html', {
        'form': form,
        'meeting': meeting
    })

@login_required
def action_item_create(request, meeting_pk):
    """View for creating action items"""
    meeting = get_object_or_404(Meeting, pk=meeting_pk)
    
    if request.method == 'POST':
        form = MeetingActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.meeting = meeting
            action.created_by = request.user
            action.save()
            messages.success(request, 'Action item created successfully.')
            return redirect('meeting_detail', pk=meeting_pk)
    else:
        form = MeetingActionForm()
        
    return render(request, 'meetings/action_form.html', {
        'form': form,
        'meeting': meeting
    })