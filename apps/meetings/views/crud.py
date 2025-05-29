# apps/meetings/views/crud.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.db import transaction
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from apps.meetings.models import Meeting, MeetingParticipant, MeetingType
from apps.meetings.forms import MeetingForm
from apps.document_management.models import Document, DocumentComment # Import DocumentComment
from apps.document_management.utils.google_drive_manager import GoogleDriveManager

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
                form.save_m2m()  # Save many-to-many relationships

                # Create participant entries
                MeetingParticipant.objects.create(
                    meeting=meeting,
                    participant=request.user,
                    role='organizer'  # Set organizer as first participant
                )
                
                for user_participant in form.cleaned_data['participants']:
                    if user_participant != request.user:  # Skip if participant is organizer
                        MeetingParticipant.objects.create(
                            meeting=meeting,
                            participant=user_participant,
                            role='attendee'
                        )

                # Handle document uploads
                if 'document_type[]' in request.POST:
                    doc_types = request.POST.getlist('document_type[]')
                    doc_files = request.FILES.getlist('document_file[]')
                    doc_notes = request.POST.getlist('document_notes[]')
                    
                    for doc_type, doc_file, notes in zip(doc_types, doc_files, doc_notes):
                        if doc_file:
                            # Create Document instance using document_management app
                            document = Document.objects.create(
                                title=doc_file.name,
                                file=doc_file,
                                uploaded_by=request.user,
                                source_module='meetings'
                            )
                            
                            # Create MeetingDocument
                            MeetingDocument.objects.create(
                                meeting=meeting,
                                document=document,
                                document_type=doc_type,
                                notes=notes
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
        'meeting_types': MeetingType.objects.filter(is_active=True)
    }
    return render(request, 'meetings/meeting_form.html', context)

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

            if not meetings_folder.get('files'):
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
                        from apps.document_management.models import DocumentComment
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
        'attachments': meeting_attachments, # Pass attachments to the template
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
            # Parse date and times
            date_str = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time', '')  # Make end_time optional
            
            # Parse the date
            meeting_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Create start datetime
            start_datetime = datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")
            
            # Create end datetime if provided
            end_datetime = None
            if end_time:
                end_datetime = datetime.strptime(f"{date_str} {end_time}", "%Y-%m-%d %H:%M")
            
            # Get meeting type
            meeting_type = get_object_or_404(MeetingType, id=request.POST.get('meeting_type'))
            
            # Create the meeting
            meeting = Meeting.objects.create(
                title=request.POST.get('title'),
                date=meeting_date,
                start_time=start_datetime,
                end_time=end_datetime,
                meeting_type=meeting_type,
                location=request.POST.get('location'),
                agenda=request.POST.get('agenda', ''),  # Make agenda optional
                organizer=request.user,
                department=request.user.departments.first()  # Use first department
            )
            
            return JsonResponse({'success': True, 'meeting_id': meeting.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


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