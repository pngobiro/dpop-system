import json # Import json for serialization
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder # For date encoding
from django.db.models import Count, Q # Import Count and Q
# No longer need Paginator
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
import datetime
import os # Import os for file extension
from django.contrib.contenttypes.models import ContentType # Import ContentType
from collections import Counter # Import Counter
from .models import Project, Task, Comment
from django.contrib.auth import get_user_model # Import User model
User = get_user_model()
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
        # --- Handle Project Creation ---
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.department = department
            project.owner = request.user
            project.save()
            # Redirect to the same page but without POST data (using GET)
            return redirect('tasks:department_task_project_list', department_id=department.id)
        # If form is invalid, it will be passed to the context below

    # --- Data Fetching & Filtering for GET request ---
    # Base queryset for all projects in the department
    all_projects_in_dept_qs = Project.objects.filter(department=department).select_related('owner').order_by('name')

    # Calculate status counts based on ALL projects in the department BEFORE filtering/searching
    project_status_counts = Counter()
    # We need to iterate to use the get_status() method efficiently here
    # Consider optimizing this if performance becomes an issue (e.g., adding a status field or denormalizing)
    all_projects_list_for_counts = list(all_projects_in_dept_qs) # Evaluate once for counting
    for project in all_projects_list_for_counts:
        status = project.get_status()
        project_status_counts[status] += 1
    total_projects_count = len(all_projects_list_for_counts) # Total count

    # Get status filter parameter
    status_filter = request.GET.get('status_filter')

    # Apply Status Filter (in Python, before passing to template)
    # Evaluate the full queryset before Python filtering
    all_projects_list = list(all_projects_in_dept_qs)
    if status_filter and status_filter in project_status_counts: # Check against calculated statuses
         projects_to_display = [p for p in all_projects_list if p.get_status() == status_filter]
    else:
         projects_to_display = all_projects_list # Show all if no valid filter
    # DataTables will handle search and pagination client-side

    # --- Prepare Context ---
    # Use IDs from all projects in the department for task/workload queries
    all_project_ids = all_projects_in_dept_qs.values_list('id', flat=True)

    my_tasks = Task.objects.filter(
        project__id__in=all_project_ids, assignee=request.user # Query based on all projects in dept
    ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'assignee').order_by('due_date', 'priority')

    today = timezone.now().date()
    due_soon_date = today + datetime.timedelta(days=7)
    due_soon_tasks = Task.objects.filter(
        project__id__in=all_project_ids, due_date__isnull=False, # Query based on all projects in dept
        due_date__gte=today, due_date__lte=due_soon_date
    ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'assignee').order_by('due_date', 'priority')

    if project_form is None: project_form = ProjectForm() # Ensure form exists for GET

    # total_projects_count calculated earlier from all_projects_list_for_counts

    # --- Calculate Workload Analysis ---
    workload_data = Task.objects.filter(
        project__id__in=all_project_ids,
        assignee__isnull=False # Only include assigned tasks
    ).exclude(
        status=Task.StatusChoices.DONE # Exclude completed tasks
    ).values(
        'assignee', # Group by assignee ID
        'assignee__username', # Get username
        'assignee__first_name',
        'assignee__last_name'
        # Add other relevant user fields if needed, e.g., 'assignee__profile__avatar'
    ).annotate(
        task_count=Count('id') # Count tasks for each assignee
    ).order_by('-task_count') # Order by highest workload first

    context = {
        'department': department,
        'projects': projects_to_display, # Pass the filtered list
        'total_projects_count': total_projects_count, # Total count for summary cards
        'project_status_counts': dict(project_status_counts), # Counts for summary cards
        'status_filter': status_filter, # Current status filter (for card highlighting)
        'my_tasks': my_tasks,
        'due_soon_tasks': due_soon_tasks,
        'workload_data': workload_data, # Add workload data to context
        'project_form': project_form,
        'today': today,
        'soon_date': due_soon_date
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

    # Prepare tasks data for Frappe Gantt
    gantt_tasks_data = []
    for task in tasks:
        # Frappe Gantt needs specific keys: id, name, start, end
        # Only include tasks with both start and end dates for the chart
        if task.start_date and task.due_date:
            gantt_tasks_data.append({
                'id': str(task.id), # ID must be a string
                'name': task.title,
                'start': task.start_date.isoformat(), # Format date as YYYY-MM-DD
                'end': task.due_date.isoformat(), # Format date as YYYY-MM-DD
                # 'progress': 50, # Optional: Add progress calculation if needed
                # 'dependencies': '' # Optional: Add dependencies if needed
            })

    context = {
        'project': project,
        'tasks': tasks, # Keep original tasks list for the table
        'project_attachments': project_attachments,
        'attachment_form': attachment_form,
        'gantt_tasks_json': json.dumps(gantt_tasks_data, cls=DjangoJSONEncoder) # Pass JSON data
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
