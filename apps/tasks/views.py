from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
import datetime
import os # Import os for file extension
from django.contrib.contenttypes.models import ContentType # Import ContentType
from .models import Project, Task, Comment
from .forms import TaskForm, CommentForm, ProjectForm

# Import Department model safely
try:
    from apps.organization.models import Department
except ImportError:
    Department = None

# Import Document model and Form safely
try:
    from apps.document_management.models import Document
    from apps.document_management.forms import DocumentForm # Import DocumentForm
except ImportError:
    Document = None
    DocumentForm = None # Set form to None if import fails

# --- Project Views ---
# (project_list, department_task_project_list views remain the same)
@login_required
def project_list(request):
    projects = Project.objects.all().select_related('department', 'owner')
    context = {'projects': projects}
    return HttpResponse(f"Placeholder: List of {projects.count()} total projects.")

@login_required
def department_task_project_list(request, department_id):
    if not Department: raise Http404("Organization app not configured correctly.")
    department = get_object_or_404(Department, pk=department_id)
    project_form = None
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.department = department
            project.owner = request.user
            project.save()
            return redirect('tasks:department_task_project_list', department_id=department.id)
    department_projects = Project.objects.filter(department=department)
    project_ids = department_projects.values_list('id', flat=True)
    my_tasks = Task.objects.filter(
        project__id__in=project_ids, assignee=request.user
    ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'assignee').order_by('due_date', 'priority')
    today = timezone.now().date()
    due_soon_date = today + datetime.timedelta(days=7)
    due_soon_tasks = Task.objects.filter(
        project__id__in=project_ids, due_date__isnull=False,
        due_date__gte=today, due_date__lte=due_soon_date
    ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'assignee').order_by('due_date', 'priority')
    if project_form is None: project_form = ProjectForm()
    context = {
        'department': department, 'projects': department_projects.select_related('owner').order_by('name'),
        'my_tasks': my_tasks, 'due_soon_tasks': due_soon_tasks, 'project_form': project_form,
        'today': today, 'soon_date': due_soon_date
    }
    return render(request, 'tasks/department_task_project_list.html', context)

@login_required
def project_detail(request, project_id):
    """
    Display details, tasks, and attachments for a specific project.
    Also handles POST requests for adding new project attachments.
    """
    project = get_object_or_404(Project.objects.select_related('department', 'owner'), pk=project_id)
    attachment_form = None # Initialize form

    if request.method == 'POST':
        # Handle new attachment submission
        if not DocumentForm:
             return HttpResponse("Document Management app not configured correctly.", status=501)

        attachment_form = DocumentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            doc = attachment_form.save(commit=False)
            doc.uploaded_by = request.user
            doc.source_module = 'tasks' # Indicate source app

            # Link to the project using GenericForeignKey fields
            doc.content_type = ContentType.objects.get_for_model(Project)
            doc.object_id = project.id

            # Extract file info (assuming local storage for now)
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                doc.file_size = uploaded_file.size
                # Basic file type extraction from extension
                name, extension = os.path.splitext(uploaded_file.name)
                doc.file_type = extension.lower().strip('.') if extension else 'unknown'
                # NOTE: For Google Drive, different logic would be needed here
                # to upload to Drive and store the ID/link instead of the file locally.
                doc.storage_type = 'local'

            doc.save()
            # Redirect back to the project detail page
            return redirect('tasks:project_detail', project_id=project.id)
        # If form invalid, it's passed to context below

    # --- Data Fetching for GET or after failed POST ---
    tasks = project.tasks.all().select_related('assignee', 'creator').order_by('priority', 'due_date')
    project_attachments = project.attachments.all() if Document and hasattr(project, 'attachments') else []

    # Create blank form for GET if not already set by failed POST
    if attachment_form is None and DocumentForm:
        attachment_form = DocumentForm()

    context = {
        'project': project,
        'tasks': tasks,
        'project_attachments': project_attachments,
        'attachment_form': attachment_form # Add attachment form to context
    }
    return render(request, 'tasks/project_detail.html', context)

# --- Task Views ---
# (task_detail needs similar update for task attachments)
@login_required
def task_detail(request, task_id):
    """
    Display details, comments, and attachments for a specific task.
    Handles adding new comments via POST.
    Handles adding new task attachments via POST.
    """
    task = get_object_or_404(Task.objects.select_related('project', 'assignee', 'creator'), pk=task_id)
    comments = task.comments.all().select_related('author').order_by('created_at')
    task_attachments = task.attachments.all() if Document and hasattr(task, 'attachments') else []
    comment_form = CommentForm() # Initialize blank forms for GET
    attachment_form = DocumentForm() if DocumentForm else None

    if request.method == 'POST':
        # Determine if it's a comment or attachment submission
        # We can use a hidden input in the forms or check button names/values
        # Simple approach: check which form has data or which button was clicked
        # For now, assume separate forms/buttons or check request content

        # Check for comment submission (e.g., check for 'content' field)
        if 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.author = request.user
                comment.save()
                return redirect('tasks:task_detail', task_id=task.id)
            # If invalid, fall through to render page with errors

        # Check for attachment submission (e.g., check for 'file' field)
        elif 'file' in request.FILES and DocumentForm:
            attachment_form = DocumentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                doc = attachment_form.save(commit=False)
                doc.uploaded_by = request.user
                doc.source_module = 'tasks'
                doc.content_type = ContentType.objects.get_for_model(Task)
                doc.object_id = task.id
                uploaded_file = request.FILES.get('file')
                if uploaded_file:
                    doc.file_size = uploaded_file.size
                    name, extension = os.path.splitext(uploaded_file.name)
                    doc.file_type = extension.lower().strip('.') if extension else 'unknown'
                    doc.storage_type = 'local'
                doc.save()
                return redirect('tasks:task_detail', task_id=task.id)
            # If invalid, fall through to render page with errors
        else:
             # Handle case where POST occurred but wasn't identifiable
             # Or maybe just re-render the page
             pass


    context = {
        'task': task, 'comments': comments, 'attachments': task_attachments,
        'comment_form': comment_form, 'attachment_form': attachment_form
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if task.project != project: return HttpResponseForbidden("Project mismatch.")
            task.creator = request.user
            task.save()
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(initial={'project': project})
    context = {'form': form, 'project': project}
    return render(request, 'tasks/add_task.html', context)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    can_edit = (request.user == task.creator or request.user == task.assignee)
    if not can_edit: return HttpResponseForbidden("You do not have permission to edit this task.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    context = {'form': form, 'task': task}
    return render(request, 'tasks/edit_task.html', context)


# Remove the separate add_attachment and add_project_attachment views
# as the logic is now integrated into the detail views.

# @login_required
# def add_attachment(request, task_id): ... (REMOVED)

# @login_required
# def add_project_attachment(request, project_id): ... (REMOVED)
