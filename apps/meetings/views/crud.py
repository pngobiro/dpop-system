# apps/meetings/views/crud.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
from apps.meetings.models import Meeting, MeetingParticipant, MeetingType
from apps.meetings.forms import MeetingForm

@login_required
def meeting_create(request):
    """Create a new meeting"""
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.organizer = request.user
            meeting.department = request.user.department
            meeting.save()
            form.save_m2m()

            # Create participant entries
            for user_participant in form.cleaned_data['participants']:
                MeetingParticipant.objects.create(
                    meeting=meeting,
                    participant=user_participant
                )

            messages.success(request, 'Meeting created successfully.')
            return redirect('meetings:meeting_detail', pk=meeting.pk)
    else:
        form = MeetingForm()

    return render(request, 'meetings/meeting_form.html', {
        'form': form, 
        'action': 'Create'
    })

@login_required
def meeting_detail(request, pk):
    """View meeting details"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    # Check permissions
    if not (user == meeting.organizer or
            user.department == meeting.department or
            meeting.participants.filter(id=user.id).exists()):
        messages.error(request, "You don't have permission to view this meeting.")
        return redirect('meetings:dashboard')

    context = {
        'meeting': meeting,
        'participants': MeetingParticipant.objects.filter(meeting=meeting),
        'can_edit': user == meeting.organizer or user.has_perm('meetings.change_meeting')
    }
    return render(request, 'meetings/meeting_detail.html', context)

@login_required
def meeting_update(request, pk):
    """Update existing meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    if not (user == meeting.organizer or user.has_perm('meetings.change_meeting')):
        messages.error(request, "You don't have permission to edit this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully.')
            return redirect('meetings:meeting_detail', pk=pk)
    else:
        form = MeetingForm(instance=meeting)

    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'meeting': meeting,
        'action': 'Update'
    })

@login_required
def meeting_delete(request, pk):
    """Delete a meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    if not (user == meeting.organizer or user.has_perm('meetings.delete_meeting')):
        messages.error(request, "You don't have permission to delete this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted successfully.')
        return redirect('meetings:dashboard')

    return render(request, 'meetings/meeting_confirm_delete.html', {
        'meeting': meeting
    })

@login_required
def add_quick_meeting(request):
    """Add a meeting quickly from calendar view"""
    if request.method == 'POST':
        try:
            # Parse the date and times
            date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            
            # Combine date and times
            start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
            
            # Get meeting type
            meeting_type = get_object_or_404(MeetingType, id=request.POST.get('meeting_type'))
            
            # Create the meeting
            meeting = Meeting.objects.create(
                title=request.POST.get('title'),
                date=date,
                start_time=start_datetime,
                end_time=end_datetime,
                meeting_type=meeting_type,
                location=request.POST.get('location'),
                agenda=request.POST.get('agenda'),
                organizer=request.user,
                department=request.user.department
            )
            
            return JsonResponse({'success': True, 'meeting_id': meeting.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})