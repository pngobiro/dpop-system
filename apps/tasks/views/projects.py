from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

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
    from apps.document_management.forms import DocumentForm
except ImportError:
    Document = None
    DocumentForm = None


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all().select_related('department', 'owner')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        status_filter = self.request.GET.get('status_filter')
        sort_by = self.request.GET.get('sort_by', 'priority') # Default sort by priority

        tasks_queryset = project.tasks.all().select_related('assignee', 'creator')

        search_query = self.request.GET.get('q')
        if search_query:
            tasks_queryset = tasks_queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        if status_filter and status_filter in dict(Task.StatusChoices.choices):
            tasks_queryset = tasks_queryset.filter(status=status_filter)

        # Apply sorting
        valid_sort_fields = ['priority', '-priority', 'due_date', '-due_date', 'title', '-title']
        if sort_by in valid_sort_fields:
            tasks_queryset = tasks_queryset.order_by(sort_by)
        else:
            tasks_queryset = tasks_queryset.order_by('priority', 'due_date') # Default sort

        context['tasks'] = tasks_queryset
        context['status_filter'] = status_filter
        context['sort_by'] = sort_by
        context['search_query'] = search_query
        context['task_status_choices'] = Task.StatusChoices.choices # For filter dropdown
        context['project_attachments'] = project.attachments.all() if Document and hasattr(project, 'attachments') else []
        context['attachment_form'] = DocumentForm() if DocumentForm else None

        gantt_tasks_data = []
        for task in context['tasks']:
            if task.start_date and task.due_date:
                gantt_tasks_data.append({
                    'id': str(task.id),
                    'name': task.title,
                    'start': task.start_date.isoformat(),
                    'end': task.due_date.isoformat(),
                })
        context['gantt_tasks_json'] = json.dumps(gantt_tasks_data, cls=DjangoJSONEncoder)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not DocumentForm:
            messages.error(request, "Document Management app not configured correctly.")
            return redirect(self.object.get_absolute_url())

        attachment_form = DocumentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            doc = attachment_form.save(commit=False)
            doc.uploaded_by = request.user
            doc.source_module = 'tasks'
            doc.content_type = ContentType.objects.get_for_model(Project)
            doc.object_id = self.object.id

            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                doc.file_size = uploaded_file.size
                name, extension = os.path.splitext(uploaded_file.name)
                doc.file_type = extension.lower().strip('.') if extension else 'unknown'
                doc.storage_type = 'local'

            doc.save()
            messages.success(request, "Attachment uploaded successfully.")
            return redirect(self.object.get_absolute_url())
        else:
            messages.error(request, "Error uploading attachment.")
            return self.get(request, *args, **kwargs) # Re-render with form errors


class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_form.html'
    success_message = "Project '%(name)s' created successfully."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_form.html'
    success_message = "Project '%(name)s' updated successfully."

    def get_success_url(self):
        return reverse_lazy('tasks:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Project
    template_name = 'tasks/project_confirm_delete.html'
    success_url = reverse_lazy('tasks:project_list')
    success_message = "Project deleted successfully."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class DepartmentProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/department_task_project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        if not Department:
            raise Http404("Organization app not configured correctly.")
        self.department = get_object_or_404(Department, pk=self.kwargs['department_id'])
        return Project.objects.filter(department=self.department).select_related('owner').order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = self.department
        context['project_form'] = ProjectForm()

        all_projects_list = list(self.get_queryset())
        project_status_counts = Counter()
        for project in all_projects_list:
            status = project.get_status()
            project_status_counts[status] += 1
        context['total_projects_count'] = len(all_projects_list)
        context['project_status_counts'] = dict(project_status_counts)

        status_filter = self.request.GET.get('status_filter')
        if status_filter and status_filter in project_status_counts:
            context['projects'] = [p for p in all_projects_list if p.get_status() == status_filter]
        else:
            context['projects'] = all_projects_list

        all_project_ids = self.get_queryset().values_list('id', flat=True)
        context['my_tasks'] = Task.objects.filter(
            project__id__in=all_project_ids, assignees=self.request.user
        ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'creator').order_by('due_date', 'priority')

        today = timezone.now().date()
        due_soon_date = today + datetime.timedelta(days=7)
        context['due_soon_tasks'] = Task.objects.filter(
            project__id__in=all_project_ids, due_date__isnull=False,
            due_date__gte=today, due_date__lte=due_soon_date
        ).exclude(status=Task.StatusChoices.DONE).select_related('project', 'creator').order_by('due_date', 'priority')

        context['today'] = today
        context['soon_date'] = due_soon_date

        context['workload_data'] = Task.objects.filter(
            project__id__in=all_project_ids,
            assignees__isnull=False
        ).exclude(
            status=Task.StatusChoices.DONE
        ).values(
            'assignees',
            'assignees__username',
            'assignees__first_name',
            'assignees__last_name'
        ).annotate(
            task_count=Count('id')
        ).order_by('-task_count')

        return context

    def post(self, request, *args, **kwargs):
        if not Department:
            raise Http404("Organization app not configured correctly.")
        self.department = get_object_or_404(Department, pk=self.kwargs['department_id'])
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.department = self.department
            project.owner = request.user
            project.save()
            messages.success(request, "Project created successfully.")
            return redirect('tasks:department_project_list', department_id=self.department.id)
        else:
            messages.error(request, "Error creating project.")
            return self.get(request, *args, **kwargs) # Re-render with form errors
