import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.db import transaction
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from apps.meetings.models import Meeting, MeetingParticipant, MeetingType, MeetingDocument
from apps.meetings.forms import MeetingForm
from apps.document_management.models import Document, DocumentComment
from apps.document_management.utils.google_drive_manager import GoogleDriveManager

logger = logging.getLogger(__name__)

@login_required
def meeting_create(request):
    """Create a new meeting"""
    initial_data = {
        'meeting_mode': 'physical',  # Set default meeting mode
    }
    
    if request.method == 'POST':
        form = MeetingForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                # Set organizer and save meeting
                meeting = form.save(commit=False)
                meeting.organizer = request.user
                meeting.department = request.user.departments.first()
                meeting.save()

                # Create organizer as first participant
                MeetingParticipant.objects.create(
                    meeting=meeting,
                    participant=request.user,
                    role='attendee'
                )

                messages.success(request, 'Meeting created successfully.')
                return redirect('meetings:meeting_detail', pk=meeting.pk)
            except Exception as e:
                messages.error(request, f'Error creating meeting: {str(e)}')
        else:
            print("Form errors:", form.errors)  # For debugging
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MeetingForm(user=request.user, initial=initial_data)

    context = {
        'form': form,
        'action': 'Create',
        'form_errors': form.errors.items(),
        'meeting_types': MeetingType.objects.filter(is_active=True),
        'current_date': timezone.now().date()
    }
    return render(request, 'meetings/meeting_form.html', context)

@login_required
def meeting_detail(request, pk):
    """View meeting details"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user
    User = get_user_model()

    # Only organizer can view their meetings
    if user != meeting.organizer:
        messages.error(request, "You don't have permission to view this meeting.")
        return redirect('meetings:dashboard')

    # Get users available to be added as participants (excluding existing participants)
    existing_participant_ids = meeting.participants.values_list('id', flat=True)
    available_users = User.objects.exclude(id__in=existing_participant_ids)

    context = {
        'meeting': meeting,
        'participants': MeetingParticipant.objects.filter(meeting=meeting),
        'can_edit': user == meeting.organizer,
        'available_users': available_users,
        'current_date': timezone.now().date()
    }
    return render(request, 'meetings/meeting_detail.html', context)

@login_required
def meeting_update(request, pk):
    """Update existing meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    if user != meeting.organizer:
        messages.error(request, "You don't have permission to edit this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        form = MeetingForm(user=request.user, data=request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully.')
            return redirect('meetings:meeting_detail', pk=pk)
    else:
        form = MeetingForm(user=request.user, instance=meeting)

    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'meeting': meeting,
        'action': 'Update'
    })

@login_required
def meeting_delete(request, pk):
    """Delete a meeting using soft delete"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    if user != meeting.organizer:
        messages.error(request, "You don't have permission to delete this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        # Use soft delete instead of changing status
        meeting.soft_delete()
        messages.success(request, 'Meeting has been deleted.')
        return redirect('meetings:dashboard')

    return render(request, 'meetings/meeting_confirm_delete.html', {
        'meeting': meeting
    })

@login_required
def add_quick_meeting(request):
    """Add a meeting quickly from calendar view"""
    if request.method == 'POST':
        logger.info("Processing quick meeting creation request")
        errors = {}
        
        # Log received data
        logger.debug(f"Received meeting data: {request.POST}")
        
        # Required fields
        title = request.POST.get('title')
        date_str = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time', '')  # Optional
        meeting_type_id = request.POST.get('meeting_type')
        meeting_mode = request.POST.get('meeting_mode', 'physical')
        physical_location = request.POST.get('location', '')
        virtual_meeting_url = request.POST.get('virtual_meeting_url', '')

        # Validate required fields
        if not title:
            errors['title'] = ['Title is required']
            logger.warning("Missing required field: title")
        if not date_str:
            errors['date'] = ['Date is required']
            logger.warning("Missing required field: date")
        if not start_time:
            errors['start_time'] = ['Start time is required']
            logger.warning("Missing required field: start_time")
        if not meeting_type_id:
            errors['meeting_type'] = ['Meeting type is required']
            logger.warning("Missing required field: meeting_type")

        # Return errors if validation failed
        if errors:
            logger.warning(f"Validation failed with errors: {errors}")
            return JsonResponse({'success': False, 'error': errors})
            
        try:
            # Parse date and times
            meeting_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            parsed_start_time = datetime.strptime(start_time, '%H:%M').time()
            parsed_end_time = datetime.strptime(end_time, '%H:%M').time() if end_time else None

            # Get meeting type
            try:
                meeting_type = MeetingType.objects.get(id=meeting_type_id)
            except MeetingType.DoesNotExist:
                logger.error(f"Invalid meeting type ID: {meeting_type_id}")
                return JsonResponse({
                    'success': False,
                    'error': {'meeting_type': ['Invalid meeting type']}
                })

            # Create meeting
            department = request.user.departments.first()
            meeting = Meeting.objects.create(
                title=title,
                date=meeting_date,
                start_time=parsed_start_time,
                end_time=parsed_end_time,
                meeting_type=meeting_type,
                meeting_mode=meeting_mode,
                physical_location=physical_location,
                virtual_meeting_url=virtual_meeting_url,
                agenda=request.POST.get('agenda', ''),  # Optional
                organizer=request.user,
                department=department
            )
            logger.info(f"Successfully created meeting with ID: {meeting.id}")

            # Add organizer as participant
            MeetingParticipant.objects.create(
                meeting=meeting,
                participant=request.user,
                role='attendee'
            )
            
            return JsonResponse({'success': True, 'meeting_id': meeting.id})
        except ValueError as e:
            logger.error(f"Date/time parsing error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': {'__all__': ['Invalid date or time format']}
            })
        except Exception as e:
            logger.error(f"Unexpected error during meeting creation: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': {'__all__': [f'Error creating meeting: {str(e)}']}
            })

    # Handle non-POST requests
    logger.warning(f"Invalid request method: {request.method}")
    return JsonResponse({
        'success': False,
        'error': {'__all__': ['Invalid request method']}
    })

@login_required
def add_meeting_participant(request, pk):
    """Add participant to an existing meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user
    User = get_user_model()

    # Only organizer can add participants
    if user != meeting.organizer:
        messages.error(request, "You don't have permission to add participants to this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        participant = request.POST.get('participant')
        role = request.POST.get('role', 'attendee')

        if participant:
            try:
                user = User.objects.get(id=participant)
                # Check if participant already exists
                if not MeetingParticipant.objects.filter(meeting=meeting, participant=user).exists():
                    MeetingParticipant.objects.create(
                        meeting=meeting,
                        participant=user,
                        role=role
                    )
                    messages.success(request, f'{user.get_full_name()} added to the meeting successfully.')
                else:
                    messages.warning(request, f'{user.get_full_name()} is already a participant.')
            except User.DoesNotExist:
                messages.error(request, "Selected user does not exist.")
            except Exception as e:
                messages.error(request, f"Error adding participant: {str(e)}")

    return redirect('meetings:meeting_detail', pk=pk)

@login_required
def add_meeting_attachment_comment(request, attachment_id):
    """Add comment to a meeting attachment"""
    if request.method == 'POST':
        attachment = get_object_or_404(Document, pk=attachment_id)
        content = request.POST.get('content')
        
        if content:
            DocumentComment.objects.create(
                document=attachment,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')

        # Redirect back to meeting detail
        meeting_id = attachment.object_id
        return redirect('meetings:meeting_detail', pk=meeting_id)

    return HttpResponseForbidden("Method not allowed")

@login_required
def meeting_action(request, pk, action):
    """Handle various meeting actions"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    # Only organizer can modify meetings
    if user != meeting.organizer:
        messages.error(request, "You don't have permission to modify this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        try:
            if action == 'cancel':
                meeting.status = 'cancelled'
                messages.success(request, 'Meeting has been cancelled.')
            
            elif action == 'start':
                meeting.status = 'in_progress'
                messages.success(request, 'Meeting has been started.')
            
            elif action == 'complete':
                meeting.status = 'completed'
                messages.success(request, 'Meeting has been marked as completed.')
            
            elif action == 'postpone':
                new_date = request.POST.get('new_date')
                new_start_time = request.POST.get('new_start_time')
                new_end_time = request.POST.get('new_end_time')
            
                if not new_date or not new_start_time:
                    messages.error(request, 'New date and start time are required for postponing.')
                    return redirect('meetings:meeting_detail', pk=pk)
                
                meeting.date = datetime.strptime(new_date, '%Y-%m-%d').date()
                meeting.start_time = datetime.strptime(new_start_time, '%H:%M').time()
                if new_end_time:
                    meeting.end_time = datetime.strptime(new_end_time, '%H:%M').time()
                
                messages.success(request, 'Meeting has been postponed.')
            
            meeting.save()
            return redirect('meetings:meeting_detail', pk=pk)
            
        except Exception as e:
            messages.error(request, f'Error updating meeting: {str(e)}')
            return redirect('meetings:meeting_detail', pk=pk)
    
    return redirect('meetings:meeting_detail', pk=pk)