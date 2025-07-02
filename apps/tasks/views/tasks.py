from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from ..models import Task, Project
from ..forms import TaskForm, CommentForm, ReassignTaskForm # Import ReassignTaskForm
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


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'pk' # Changed from task_id to pk for consistency with CBVs

    def get_queryset(self):
        return Task.objects.select_related('project', 'creator').prefetch_related('assignees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        content_type = ContentType.objects.get_for_model(Task)
        context['attachments'] = Document.objects.filter(
            content_type=content_type,
            object_id=task.id
        ).prefetch_related('comments').order_by('-created_at')
        context['reassign_form'] = ReassignTaskForm(initial={'assignees': task.assignees.all()}) # Pass form to context

        referring_url = self.request.META.get('HTTP_REFERER')
        back_button_text = "Back to Dashboard" # Default text

        if referring_url:
            if '/tasks/assigned/' in referring_url:
                back_button_text = "Back to Tasks Assigned to Me"
            elif '/tasks/created_by_me/' in referring_url:
                back_button_text = "Back to Tasks I Assigned"

        context['referring_url'] = referring_url
        context['back_button_text'] = back_button_text
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'file' in request.FILES:
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

                # Get or create directorate folder
                directorate_name = request.user.department.name if request.user.department else 'Uncategorized'
                # Remove special characters and replace spaces with underscores
                directorate_name = ''.join(c if c.isalnum() or c.isspace() else '_' for c in directorate_name)
                directorate_name = directorate_name.replace(' ', '_')
                directorate_folder = drive_manager.service.files().list(
                    q=f"name='{directorate_name}' and mimeType='application/vnd.google-apps.folder' and '{tasks_folder_id}' in parents",
                    fields='files(id, name)',
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True
                ).execute()

                directorate_files = directorate_folder.get('files', [])
                if not directorate_files:
                    directorate_folder_id = drive_manager.create_folder(directorate_name, tasks_folder_id)
                else:
                    directorate_folder_id = directorate_files[0]['id']

                # Upload file to directorate folder
                filename = f"Task_{self.object.id}_{self.object.title[:20]}_{uploaded_file.name}"
                file_id, web_link = drive_manager.upload_file(
                    file_obj=uploaded_file,
                    filename=filename,
                    folder_id=directorate_folder_id  # Upload to directorate folder
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
                            object_id=self.object.id,
                            description=f"Attachment for Task: {self.object.title}"
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
                        return redirect(self.object.get_absolute_url())

                    messages.success(request, 'File uploaded successfully to Google Drive')

                else:
                    messages.error(request, 'Failed to upload file to Google Drive')
            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')

            return redirect(self.object.get_absolute_url())
        return self.get(request, *args, **kwargs) # Re-render with form errors if not file upload


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.kwargs.get('project_pk') # Changed from project_id to project_pk
        if project_id:
            initial['project'] = get_object_or_404(Project, pk=project_id)
        return initial

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)

        # Handle related meeting
        related_meeting = form.cleaned_data.get('related_meeting')
        if related_meeting:
            form.instance.content_type = ContentType.objects.get_for_model(related_meeting)
            form.instance.object_id = related_meeting.pk
            form.instance.save(update_fields=['content_type', 'object_id'])

        messages.success(self.request, "Task created successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.pk})


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit_task.html'
    pk_url_kwarg = 'pk' # Changed from task_id to pk

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.creator or task.assignees.filter(id=self.request.user.id).exists()

    def form_valid(self, form):
        # Handle related meeting
        related_meeting = form.cleaned_data.get('related_meeting')
        if related_meeting:
            self.object.content_type = ContentType.objects.get_for_model(related_meeting)
            self.object.object_id = related_meeting.pk
        else:
            # If related meeting is cleared, clear generic relation fields
            self.object.content_type = None
            self.object.object_id = None

        messages.success(self.request, "Task updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.pk})


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
        return redirect('tasks:task_detail', pk=task_id) # Changed task_id to pk
    
    return HttpResponseForbidden("Method not allowed")


@login_required
def revert_task_to_history(request, pk, history_id):
    """Revert a task to a specific historical state"""
    from ..models import TaskHistory
    from django.contrib.auth import get_user_model
    User = get_user_model()
    task = get_object_or_404(Task, pk=pk) # Changed task_id to pk
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
        # Temporarily disable signals to prevent history loop
        from django.db.models import signals
        from apps.tasks.signals import task_post_save # Import the signal handler
        signals.post_save.disconnect(sender=Task, receiver=task_post_save)
        task.save()
        signals.post_save.connect(sender=Task, receiver=task_post_save)

        messages.success(request, f'Task reverted to state from {history_item.timestamp}.')
        return redirect('tasks:task_detail', pk=task.pk) # Changed task_id to pk

    return HttpResponseForbidden("Method not allowed")


@login_required
def update_task_status(request, pk):
    """Update the status of a task"""
    task = get_object_or_404(Task, pk=pk) # Changed task_id to pk

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in Task.StatusChoices:
            task.status = new_status
            # The history logging is now handled by the signal
            task.save()
            messages.success(request, f'Task status updated to {task.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status selected.')

        return redirect('tasks:task_detail', pk=task.pk) # Changed task_id to pk

    return HttpResponseForbidden("Method not allowed")


@login_required
def reassign_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check permissions: Only creator or project owner can reassign
    # You might want to expand this logic based on your permission system
    if not (request.user == task.creator or request.user == task.project.owner):
        messages.error(request, "You do not have permission to reassign this task.")
        return redirect('tasks:task_detail', pk=task.pk)

    if request.method == 'POST':
        form = ReassignTaskForm(request.POST, instance=task) # Pass instance to form
        if form.is_valid():
            # Manually update the many-to-many field
            new_assignees = form.cleaned_data['assignees']
            task.assignees.set(new_assignees) # .set() handles adding/removing
            
            # The signals will handle history and notifications
            # No need to call task.save() here if only M2M is changed, but if other fields were in form, you would.
            # For M2M, .set() triggers post_save for the relationship.

            messages.success(request, "Task assignees updated successfully.")
            return redirect('tasks:task_detail', pk=task.pk)
        else:
            messages.error(request, "Error reassigning task.")
            # If form is invalid, re-render the task detail page with errors
            # This requires passing the form back to the template
            return redirect('tasks:task_detail', pk=task.pk) # Simplified for now
    
    return HttpResponseForbidden("Method not allowed") # Should only be accessed via POST