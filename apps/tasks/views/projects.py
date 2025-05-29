from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.contrib.contenttypes.models import ContentType
import json
from django.core.serializers.json import DjangoJSONEncoder
from collections import Counter
import os
from django.utils import timezone
import datetime
from django.db.models import Count
from ..models import Project, Task
from ..forms import ProjectForm
try:
    from apps.organization.models import Department
except ImportError:
    Department = None

try:
    from apps.document_management.models import Document
except ImportError:
    Document = None

try:
    from apps.document_management.forms import DocumentForm
except ImportError:
    DocumentForm = None

@login_required
def project_list(request):
    projects = Project.objects.all().select_related('department', 'owner')
    context = {'projects': projects}
    return HttpResponse(f"Placeholder: List of {projects.count()} total projects.")

@login_required
def department_task_project_list(request, department_id):
    if not Department: 
        raise Http404("Organization app not configured correctly.")
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

    all_projects_in_dept_qs = Project.objects.filter(department=department).select_related('owner').order_by('name')
    project_status_counts = Counter()
    all_projects_list_for_counts = list(all_projects_in_dept_qs)
    
    for project in all_projects_list_for_counts:
        status = project.get_status()
        project_status_counts[status] += 1
    total_projects_count = len(all_projects_list_for_counts)

    status_filter = request.GET.get('status_filter')
    all_projects_list = list(all_projects_in_dept_qs)
    
    if status_filter and status_filter in project_status_counts:
        projects_to_display = [p for p in all_projects_list if p.get_status() == status_filter]
    else:
        projects_to_display = all_projects_list

    all_project_ids = all_projects_in_dept_qs.values_list('id', flat=True)
    my_tasks = Task.objects.filter(
        project__id__in=all_project_ids, assignee=request.user
    ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'assignee').order_by('due_date', 'priority')

    today = timezone.now().date()
    due_soon_date = today + datetime.timedelta(days=7)
    due_soon_tasks = Task.objects.filter(
        project__id__in=all_project_ids, due_date__isnull=False,
        due_date__gte=today, due_date__lte=due_soon_date
    ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'assignee').order_by('due_date', 'priority')

    if project_form is None: 
        project_form = ProjectForm()

    workload_data = Task.objects.filter(
        project__id__in=all_project_ids,
        assignee__isnull=False
    ).exclude(
        status=Task.StatusChoices.DONE
    ).values(
        'assignee',
        'assignee__username',
        'assignee__first_name',
        'assignee__last_name'
    ).annotate(
        task_count=Count('id')
    ).order_by('-task_count')

    context = {
        'department': department,
        'projects': projects_to_display,
        'total_projects_count': total_projects_count,
        'project_status_counts': dict(project_status_counts),
        'status_filter': status_filter,
        'my_tasks': my_tasks,
        'due_soon_tasks': due_soon_tasks,
        'workload_data': workload_data,
        'project_form': project_form,
        'today': today,
        'soon_date': due_soon_date
    }
    return render(request, 'tasks/department_task_project_list.html', context)

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project.objects.select_related('department', 'owner'), pk=project_id)
    attachment_form = None

    if request.method == 'POST':
        if not DocumentForm:
            return HttpResponse("Document Management app not configured correctly.", status=501)

        attachment_form = DocumentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            doc = attachment_form.save(commit=False)
            doc.uploaded_by = request.user
            doc.source_module = 'tasks'
            doc.content_type = ContentType.objects.get_for_model(Project)
            doc.object_id = project.id

            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                doc.file_size = uploaded_file.size
                name, extension = os.path.splitext(uploaded_file.name)
                doc.file_type = extension.lower().strip('.') if extension else 'unknown'
                doc.storage_type = 'local'

            doc.save()
            return redirect('tasks:project_detail', project_id=project.id)

    tasks = project.tasks.all().select_related('assignee', 'creator').order_by('priority', 'due_date')
    project_attachments = project.attachments.all() if Document and hasattr(project, 'attachments') else []

    if attachment_form is None and DocumentForm:
        attachment_form = DocumentForm()

    gantt_tasks_data = []
    for task in tasks:
        if task.start_date and task.due_date:
            gantt_tasks_data.append({
                'id': str(task.id),
                'name': task.title,
                'start': task.start_date.isoformat(),
                'end': task.due_date.isoformat(),
            })

    context = {
        'project': project,
        'tasks': tasks,
        'project_attachments': project_attachments,
        'attachment_form': attachment_form,
        'gantt_tasks_json': json.dumps(gantt_tasks_data, cls=DjangoJSONEncoder)
    }
    return render(request, 'tasks/project_detail.html', context)