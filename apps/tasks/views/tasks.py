from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from ..models import Task, Project
from ..forms import TaskForm, CommentForm
from apps.document_management.utils.google_drive_manager import GoogleDriveManager
try:
    from apps.document_management.forms import DocumentForm
except ImportError:
    DocumentForm = None

try:
    from apps.document_management.models import Document
except ImportError:
    Document = None
    DocumentForm = None

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task.objects.select_related('project', 'creator').prefetch_related('assignees'), pk=task_id)
    content_type = ContentType.objects.get_for_model(Task)
    task_attachments = Document.objects.filter(
        content_type=content_type,
        object_id=task.id
    ).prefetch_related('comments').order_by('-created_at')

    if request.method == 'POST' and 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            drive_manager = GoogleDriveManager()
            
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

                # Upload file directly to Tasks folder
                filename = f"Task_{task.id}_{task.title[:20]}_{uploaded_file.name}"
                file_id, web_link = drive_manager.upload_file(
                    file_obj=uploaded_file,
                    filename=filename,
                    folder_id=tasks_folder_id
                )
                
                if file_id and web_link:
                    try:
                        content_type = ContentType.objects.get_for_model(Task)
                        # Create document
                        doc = Document.objects.create(
                            title=uploaded_file.name,
                            file_size=uploaded_file.size,
                            file_type=uploaded_file.content_type,
                            storage_type='google_drive',
                            drive_file_id=file_id,
                            drive_view_link=web_link,  # Fixed field name
                            file=None,  # Set to None for Google Drive files
                            uploaded_by=request.user,
                            source_module='tasks',
                            content_type=content_type,
                            object_id=task.id,
                            description=f"Attachment for Task: {task.title}"
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
                        return redirect('tasks:task_detail', task_id=task.id)

                    messages.success(request, 'File uploaded successfully to Google Drive')

                else:
                    messages.error(request, 'Failed to upload file to Google Drive')
            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')

            return redirect('tasks:task_detail', task_id=task.id)

    context = {
        'task': task,
        'attachments': task_attachments
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if task.project != project:
                return HttpResponseForbidden("Project mismatch.")
            task.creator = request.user
            task.save()
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(initial={'project': project})
    
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'tasks/add_task.html', context)

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    can_edit = (request.user == task.creator or task.assignees.filter(id=request.user.id).exists())
    if not can_edit:
        return HttpResponseForbidden("You do not have permission to edit this task.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task
    }
    return render(request, 'tasks/edit_task.html', context)

@login_required
def add_attachment_comment(request, attachment_id):
    """Add comment to an attachment"""
    if request.method == 'POST':
        from apps.document_management.models import Document, DocumentComment
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
            
        # Redirect back to task detail
        task_id = attachment.object_id  # Get the task ID from the attachment's generic relation
        return redirect('tasks:task_detail', task_id=task_id)
    
    return HttpResponseForbidden("Method not allowed")

@login_required
def revert_task_to_history(request, task_id, history_id):
    """Revert a task to a specific historical state"""
    from ..models import TaskHistory
    from django.contrib.auth import get_user_model
    User = get_user_model()
    task = get_object_or_404(Task, pk=task_id)
    history_item = get_object_or_404(TaskHistory, pk=history_id, task=task)

    if request.method == 'POST':
        task_state = history_item.task_state
        task.title = task_state['title']
        task.description = task_state['description']
        task.status = task_state['status']
        task.priority = task_state['priority']
        
        # Clear existing assignees and re-assign
        task.assignees.clear()
        for assignee_id in task_state['assignees']:
            try:
                assignee = User.objects.get(id=assignee_id)
                task.assignees.add(assignee)
            except User.DoesNotExist:
                messages.error(request, f'Assignee with ID {assignee_id} not found.')

        task.due_date = task_state['due_date']
        task.save()

        messages.success(request, f'Task reverted to state from {history_item.timestamp}.')
        return redirect('tasks:task_detail', task_id=task_id)

    return HttpResponseForbidden("Method not allowed")

@login_required
def update_task_status(request, task_id):
    """Update the status of a task and log the change in history"""
    task = get_object_or_404(Task, pk=task_id)
    old_status = task.get_status_display()  # Get display value before change

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in Task.StatusChoices:
            task.status = new_status
            task.save()

            # Log the status change in TaskHistory
            from ..models import TaskHistory
            TaskHistory.objects.create(
                task=task,
                user=request.user,
                task_state={
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'priority': task.priority,
                    'assignees': [assignee.id for assignee in task.assignees.all()],
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                },
                comment=f'Status changed from {old_status} to {task.get_status_display()}'
            )
            messages.success(request, f'Task status updated to {task.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status selected.')

        return redirect('tasks:task_detail', task_id=task_id)

    return HttpResponseForbidden("Method not allowed")