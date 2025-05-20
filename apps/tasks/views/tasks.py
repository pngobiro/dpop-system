from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from ..models import Task
from ..forms import TaskForm, CommentForm
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
    task = get_object_or_404(Task.objects.select_related('project', 'assignee', 'creator'), pk=task_id)
    comments = task.comments.all().select_related('author').order_by('created_at')
    task_attachments = task.attachments.all() if Document and hasattr(task, 'attachments') else []
    comment_form = CommentForm()
    attachment_form = DocumentForm() if DocumentForm else None

    if request.method == 'POST':
        if 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.author = request.user
                comment.save()
                return redirect('tasks:task_detail', task_id=task.id)

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

    context = {
        'task': task,
        'comments': comments,
        'attachments': task_attachments,
        'comment_form': comment_form,
        'attachment_form': attachment_form
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
    can_edit = (request.user == task.creator or request.user == task.assignee)
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