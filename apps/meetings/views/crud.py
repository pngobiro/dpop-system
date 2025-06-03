# apps/meetings/views/crud.py
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
    # Ensure user has a department before proceeding
    if not request.user.department:
        messages.error(request, "You must be assigned to a department to create meetings.")
        return redirect('meetings:dashboard')

    initial_data = {
        'meeting_mode': 'physical',  # Set default meeting mode
        'department': request.user.department.id  # Set user's department ID as initial value
    }
    
    if request.method == 'POST':
        form = MeetingForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                # Set organizer and save meeting
                meeting = form.save(commit=False)
                meeting.organizer = request.user
                # Override department with user's first department
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

    # Check permissions
    if not (user == meeting.organizer or
            user.department == meeting.department or
            meeting.participants.filter(id=user.id).exists()):
        messages.error(request, "You don't have permission to view this meeting.")
        return redirect('meetings:dashboard')

    # Get users available to be added as participants (excluding existing participants)
    existing_participant_ids = meeting.participants.values_list('id', flat=True)
    available_users = User.objects.exclude(id__in=existing_participant_ids)

    content_type = ContentType.objects.get_for_model(Meeting)
    meeting_attachments = Document.objects.filter(
        content_type=content_type,
        object_id=meeting.id
    ).prefetch_related('comments').order_by('-created_at')

    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        drive_manager = GoogleDriveManager()

        try:
            # Get or create Meetings folder
            meetings_folder_name = 'Meetings'
            meetings_folder = drive_manager.service.files().list(
                q=f"name='{meetings_folder_name}' and mimeType='application/vnd.google-apps.folder' and '{drive_manager.DEFAULT_FOLDER_ID}' in parents",
                fields='files(id, name)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            files = meetings_folder.get('files', [])
            if not files:
                meetings_folder_id = drive_manager.create_folder(meetings_folder_name, drive_manager.DEFAULT_FOLDER_ID)
            else:
                meetings_folder_id = meetings_folder['files'][0]['id']

            # Upload file directly to Meetings folder
            filename = f"Meeting_{meeting.id}_{meeting.title[:20]}_{uploaded_file.name}"
            file_id, web_link = drive_manager.upload_file(
                file_obj=uploaded_file,
                filename=filename,
                folder_id=meetings_folder_id
            )

            if file_id and web_link:
                try:
                    content_type = ContentType.objects.get_for_model(Meeting)
                    # Create document
                    doc = Document.objects.create(
                        title=uploaded_file.name,
                        file_size=uploaded_file.size,
                        file_type=uploaded_file.content_type,
                        storage_type='google_drive',
                        drive_file_id=file_id,
                        drive_view_link=web_link,
                        file=None,  # Set to None for Google Drive files
                        uploaded_by=request.user,
                        source_module='meetings',
                        content_type=content_type,
                        object_id=meeting.id,
                        description=f"Attachment for Meeting: {meeting.title}"
                    )

                    # Create initial comment if provided
                    initial_comment = request.POST.get('initial_comment')
                    if initial_comment:
                        DocumentComment.objects.create(
                            document=doc,
                            author=request.user,
                            content=initial_comment
                        )
                except Exception as e:
                    messages.error(request, f'Error uploading file: {str(e)}')
                    return redirect('meetings:meeting_detail', pk=meeting.pk)

                messages.success(request, 'File uploaded successfully to Google Drive')

            else:
                messages.error(request, 'Failed to upload file to Google Drive')
        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')

        return redirect('meetings:meeting_detail', pk=meeting.pk)

    context = {
        'meeting': meeting,
        'participants': MeetingParticipant.objects.filter(meeting=meeting),
        'can_edit': user == meeting.organizer or user.has_perm('meetings.change_meeting'),
        'attachments': meeting_attachments,
        'available_users': available_users,
        'current_date': timezone.now().date()
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
    current_date = timezone.now().date()
    """Add a meeting quickly from calendar view"""
    # Ensure user has a department before proceeding
    if not request.user.department:
        logger.warning("User does not have a department assigned")
        return JsonResponse({
            'success': False,
            'error': {'__all__': ['You must be assigned to a department to create meetings.']}
        })

    if request.method == 'POST':
        logger.info("Processing quick meeting creation request")
        errors = {}
        
        # Log received data
        logger.debug(f"Received meeting data: {request.POST}")
        
        # Validate required fields
        title = request.POST.get('title')
        if not title:
            errors['title'] = ['Title is required']
        logger.warning("Missing required field: title")
            
        # Validate date and times
        date_str = request.POST.get('date')
        if not date_str:
            errors['date'] = ['Date is required']
            logger.warning("Missing required field: date")
            
        start_time = request.POST.get('start_time')
        if not start_time:
            errors['start_time'] = ['Start time is required']
            logger.warning("Missing required field: start_time")
            
        end_time = request.POST.get('end_time', '')  # Optional
        
        # Try parsing date and times if provided
        try:
            if date_str and start_time:
                meeting_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                start_datetime = datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")
                if end_time:
                    end_datetime = datetime.strptime(f"{date_str} {end_time}", "%Y-%m-%d %H:%M")
                    # Compare only the time portion
                    start_time_only = start_datetime.time()
                    end_time_only = end_datetime.time()
                    if start_time_only >= end_time_only:
                        errors['end_time'] = ['End time must be after start time']
                        logger.warning(f"Invalid end time: {end_time} is before or equal to start time {start_time}")
        except ValueError as e:
            errors['date'] = ['Invalid date or time format']
            logger.error(f"Date/time parsing error: {str(e)}")
            
        # Validate meeting type
        meeting_type_id = request.POST.get('meeting_type')
        if not meeting_type_id:
            errors['meeting_type'] = ['Meeting type is required']
            logger.warning("Missing required field: meeting_type")
        else:
            try:
                meeting_type = MeetingType.objects.get(id=meeting_type_id)
                logger.debug(f"Found meeting type: {meeting_type.name}")
            except MeetingType.DoesNotExist:
                errors['meeting_type'] = ['Invalid meeting type']
                logger.error(f"Invalid meeting type ID: {meeting_type_id}")
                
        # Validate meeting mode and location fields
        meeting_mode = request.POST.get('meeting_mode', 'physical')
        physical_location = request.POST.get('location', '')
        virtual_meeting_url = request.POST.get('virtual_meeting_url', '')
        
        logger.debug(f"Meeting mode: {meeting_mode}")
        if meeting_mode in ['virtual', 'hybrid'] and not virtual_meeting_url:
            errors['virtual_meeting_url'] = ['Virtual meeting URL is required for virtual/hybrid meetings']
            logger.warning(f"Missing virtual meeting URL for {meeting_mode} meeting")
        if meeting_mode in ['physical', 'hybrid'] and not physical_location:
            errors['location'] = ['Physical location is required for physical/hybrid meetings']
            logger.warning(f"Missing physical location for {meeting_mode} meeting")
            
        # Return errors if any validation failed
        if errors:
            logger.warning(f"Validation failed with errors: {errors}")
            return JsonResponse({'success': False, 'error': errors})
        
        logger.info("All validation passed, creating meeting")
        try:
            
            # Create meeting with all fields
            logger.info(f"Creating meeting with title: {title}, mode: {meeting_mode}")
            logger.info(f"request.user.departments: {request.user.departments}")
            logger.info(f"request.user.departments.first(): {request.user.departments.first()}")
            meeting = Meeting.objects.create(
                title=title,
                date=meeting_date,
                start_time=start_time,
                end_time=end_time if end_time else None,
                meeting_type=meeting_type,
                meeting_mode=meeting_mode,
                physical_location=physical_location,
                virtual_meeting_url=virtual_meeting_url,
                agenda=request.POST.get('agenda', ''),  # Optional
                organizer=request.user,
                department=request.user.departments.first()
            )
            if meeting.department is None:
                logger.error("Department is None, meeting creation failed")
                return JsonResponse({
                    'success': False,
                    'error': {'__all__': ['Error creating meeting: Department is required.']}
                })
            logger.info(f"Successfully created meeting with ID: {meeting.id}")

            # Add organizer as participant
            logger.debug(f"Adding organizer {request.user.username} as participant")
            MeetingParticipant.objects.create(
                meeting=meeting,
                participant=request.user,
                role='attendee'
            )
            logger.info(f"Successfully added organizer to meeting {meeting.id}")
            
            return JsonResponse({'success': True, 'meeting_id': meeting.id})
        except Exception as e:
            # Catch any other unexpected errors
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
        meeting_id = attachment.object_id  # Get the meeting ID from the attachment's generic relation
        return redirect('meetings:meeting_detail', pk=meeting_id)

    return HttpResponseForbidden("Method not allowed")

@login_required
def add_meeting_participant(request, pk):
    """Add participant to an existing meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user
    User = get_user_model()

    # Check if user is organizer or has permission
    if not (user == meeting.organizer or user.has_perm('meetings.change_meeting')):
        messages.error(request, "You don't have permission to add participants to this meeting.")
        return redirect('meetings:meeting_detail', pk=pk)

    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        role = request.POST.get('role', 'attendee')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        if participant_id:
            try:
                participant = User.objects.get(id=participant_id)
                # Check if participant already exists
                if not MeetingParticipant.objects.filter(meeting=meeting, participant=participant).exists():
                    MeetingParticipant.objects.create(
                        meeting=meeting,
                        participant=participant,
                        role=role
                    )
                    messages.success(request, f'{participant.get_full_name()} added to the meeting successfully.')
                else:
                    messages.warning(request, f'{participant.get_full_name()} is already a participant.')

            except User.DoesNotExist:
                messages.error(request, "Selected user does not exist.")
            except Exception as e:
                messages.error(request, f"Error adding participant: {str(e)}")
        else:
            # Adding a non-staff participant
            if not name or not email:
                messages.error(request, "Name and email are required for non-staff participants.")
            else:
                try:
                    MeetingParticipant.objects.create(
                        meeting=meeting,
                        name=name,
                        email=email,
                        mobile=mobile,
                        role=role,
                        is_external=True
                    )
                    messages.success(request, f'{name} added to the meeting successfully.')
                except Exception as e:
                    messages.error(request, f"Error adding participant: {str(e)}")

    return redirect('meetings:meeting_detail', pk=pk)

@login_required
def meeting_action(request, pk, action):
    """Handle various meeting actions: postpone, cancel, start, complete"""
    meeting = get_object_or_404(Meeting, pk=pk)
    user = request.user

    # Check permissions
    if not (request.user == meeting.organizer or request.user.has_perm('meetings.change_meeting')):
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
            
            # Redirect back to meeting detail
            return redirect('meetings:meeting_detail', pk=pk)
            
        except Exception as e:
            messages.error(request, f'Error updating meeting: {str(e)}')
            return redirect('meetings:meeting_detail', pk=pk)
    
    return redirect('meetings:meeting_detail', pk=pk)