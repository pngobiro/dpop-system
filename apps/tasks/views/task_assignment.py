"""
Task assignment and creation views.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from authentication.models import CustomUser
from apps.tasks.models import Task, Project
from apps.meetings.models import Meeting
from apps.document_management.models import Document
import datetime


@login_required
def assign_task(request):
    """Handle assigning a new task"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignee_ids = request.POST.getlist('assignees[]')
        due_date_str = request.POST.get('due_date')
        project_id = request.POST.get('project')
        related_meeting_id = request.POST.get('related_meeting')
        files = request.FILES.getlist('attachments[]')

        # Validate required fields
        if not all([title, description, due_date_str, project_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('tasks:tasks_assigned_by_me')

        try:
            project = Project.objects.get(id=project_id)
            
            # --- Permission Check for Task Assignment ---
            can_assign = False
            # 1. Global Administrator
            if request.user.is_superuser or request.user.is_staff:
                can_assign = True
            # 2. Project Owner (can assign tasks within their project)
            elif request.user == project.owner:
                can_assign = True
            # 3. Department Head/Manager (can assign tasks within their department)
            elif request.user.department and project.department and \
                 request.user.department == project.department and \
                 (request.user.is_director or request.user.is_manager):
                can_assign = True

            if not can_assign:
                messages.error(request, "You do not have permission to assign tasks in this project or department.")
                return redirect('tasks:tasks_assigned_by_me')

            # Convert due_date string to date object
            try:
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                messages.error(request, 'Invalid due date format.')
                return redirect('tasks:tasks_assigned_by_me')

            # Create the base task
            task = Task.objects.create(
                project=project,
                title=title,
                description=description,
                creator=request.user,
                due_date=due_date
            )

            # Handle related meeting
            if related_meeting_id:
                try:
                    related_meeting = Meeting.objects.get(id=related_meeting_id)
                    task.content_type = ContentType.objects.get_for_model(related_meeting)
                    task.object_id = related_meeting.pk
                    task.save(update_fields=['content_type', 'object_id'])
                except Meeting.DoesNotExist:
                    messages.warning(request, "Related meeting not found.")
                except Exception as e:
                    messages.error(request, f"Error linking task to meeting: {e}")

            # Handle assignees
            assigned_users = []

            # Add other assignees
            for assignee_id in assignee_ids:
                try:
                    assignee = CustomUser.objects.get(id=assignee_id)
                    task.assignees.add(assignee)
                    assigned_users.append(assignee.get_full_name() or assignee.username)
                except CustomUser.DoesNotExist:
                    messages.warning(request, f'User with ID {assignee_id} not found.')

            # Handle "Assign to myself" option
            if request.POST.get('assign_to_self') == 'on': # Checkbox value is 'on' if checked
                if str(request.user.id) not in assignee_ids: # Only add if not already selected in multi-select
                    task.assignees.add(request.user)
                    assigned_users.append(request.user.get_full_name() or request.user.username)

            # Handle file attachments using Google Drive
            _handle_task_attachments(request, task, files)

            # Success message
            assignee_list = ", ".join(assigned_users)
            attachment_count = len([f for f in files if f.size <= 10 * 1024 * 1024])
            messages.success(
                request,
                f'Task "{title}" has been successfully assigned to {assignee_list}. '
                f'Due date: {task.due_date.strftime("%B %d, %Y")}. '
                f'{attachment_count} file(s) attached.'
            )

        except Project.DoesNotExist:
            messages.error(request, 'Selected project does not exist.')
        except ValueError as ve:
            messages.error(request, f'Invalid data provided: {str(ve)}')
        except Exception as e:
            messages.error(request, f'Error assigning task: {str(e)}')

    return redirect('tasks:tasks_assigned_by_me')


def _handle_task_attachments(request, task, files):
    """
    Handle file attachments for a task using Google Drive.
    
    Args:
        request: Django request object
        task: Task instance
        files: List of uploaded files
    """
    from apps.document_management.utils.google_drive_manager import GoogleDriveManager
    
    drive_manager = GoogleDriveManager()
    
    for file in files:
        if file.size <= 10 * 1024 * 1024:  # 10MB limit
            try:
                # Get or create Tasks folder
                tasks_folder_name = 'Tasks'
                tasks_folder = drive_manager.service.files().list(
                    q=f"name='{tasks_folder_name}' and mimeType='application/vnd.google-apps.folder' and '{drive_manager.DEFAULT_FOLDER_ID}' in parents",
                    fields='files(id, name)',
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True
                ).execute()

                if not tasks_folder.get('files'):
                    tasks_folder_id = drive_manager.create_folder(tasks_folder_name, drive_manager.DEFAULT_FOLDER_ID)
                else:
                    tasks_folder_id = tasks_folder['files'][0]['id']

                # Upload file to Google Drive
                filename = f"Task_{task.id}_{task.title[:20]}_{file.name}"
                file_id, web_link = drive_manager.upload_file(
                    file_obj=file,
                    filename=filename,
                    folder_id=tasks_folder_id
                )
                
                if file_id and web_link:
                    Document.objects.create(
                        title=file.name,
                        file_type=file.content_type,
                        file_size=file.size,
                        storage_type='google_drive',
                        drive_file_id=file_id,
                        drive_view_link=web_link,
                        content_type=ContentType.objects.get_for_model(task),
                        object_id=task.id,
                        source_module='tasks',
                        uploaded_by=request.user,
                        description=f"Attachment for Task: {task.title}"
                    )
            except Exception as e:
                messages.error(request, f'Error uploading file {file.name}: {str(e)}')
        else:
            messages.warning(request, f'File {file.name} exceeds 10MB limit and was not uploaded.')
