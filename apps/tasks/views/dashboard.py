from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from authentication.models import CustomUser
from apps.tasks.models import Task, Project
from apps.meetings.models import Meeting
from apps.document_management.models import Document

@login_required
def user_tasks_dashboard(request):
    """Dashboard showing user's tasks"""
    today = timezone.now().date()
    
    # Get tasks assigned to the user
    assigned_tasks = Task.objects.filter(assignee=request.user).select_related('project').order_by('due_date')
    
    # Tasks created by the user
    created_tasks = Task.objects.filter(creator=request.user).select_related('project').order_by('due_date')
    
    # Pending tasks (not done)
    pending_tasks = assigned_tasks.exclude(status=Task.StatusChoices.DONE)
    
    # Overdue tasks
    overdue_tasks = pending_tasks.filter(due_date__lt=today)
    
    # Tasks due today
    due_today = pending_tasks.filter(due_date=today)
    
    # Recently completed tasks
    completed_tasks = assigned_tasks.filter(
        status=Task.StatusChoices.DONE
    ).order_by('-updated_at')[:5]
    
    context = {
        'assigned_tasks': assigned_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'due_today': due_today,
        'completed_tasks': completed_tasks,
        'created_tasks': created_tasks,
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required
def my_dashboard(request):
    """Dashboard showing user's tasks, meetings, and documents"""
    today = timezone.now().date()
    
    # Get tasks assigned to me with detailed stats
    my_tasks = Task.objects.filter(assignee=request.user)
    my_tasks_stats = {
        'total': my_tasks.count(),
        'pending': my_tasks.exclude(status=Task.StatusChoices.DONE).count(),
        'completed': my_tasks.filter(status=Task.StatusChoices.DONE).count(),
        'overdue': my_tasks.exclude(status=Task.StatusChoices.DONE).filter(due_date__lt=today).count(),
        'due_today': my_tasks.exclude(status=Task.StatusChoices.DONE).filter(due_date=today).count()
    }
    
    # Get tasks I assigned to others
    tasks_i_assigned = Task.objects.filter(creator=request.user)
    assigned_tasks_stats = {
        'total': tasks_i_assigned.count(),
        'pending': tasks_i_assigned.exclude(status=Task.StatusChoices.DONE).count(),
        'completed': tasks_i_assigned.filter(status=Task.StatusChoices.DONE).count()
    }
    
    # Get meetings stats
    all_meetings = Meeting.objects.all()
    meetings_stats = {
        'upcoming': Meeting.objects.filter(date__gte=today).count(),
        'today': Meeting.objects.filter(date=today).count(),
        'this_week': Meeting.objects.filter(date__gte=today, date__lte=today + timezone.timedelta(days=7)).count()
    }
    
    context = {
        'my_tasks_stats': my_tasks_stats,
        'assigned_tasks_stats': assigned_tasks_stats,
        'meetings_stats': meetings_stats,
        'document_count': 0 #Document.objects.count()
    }
    return render(request, 'tasks/my_dashboard.html', context)


@login_required
def tasks_assigned_by_me(request):
    """View for tasks that the user has assigned to others"""
    tasks = Task.objects.filter(
        creator=request.user
    ).select_related(
        'assignee', 'project'
    ).order_by('-created_at')

    # Get all users for the assign task modal
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()
    
    context = {
        'tasks': tasks,
        'title': 'Tasks I Assigned',
        'users': users,
        'projects': projects,
        'request': request,
    }
    return render(request, 'tasks/tasks_assigned.html', context)


@login_required
def assign_task(request):
    """Handle assigning a new task to someone"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignee_ids = request.POST.getlist('assignees[]')
        due_date = request.POST.get('due_date')
        project_id = request.POST.get('project')
        files = request.FILES.getlist('attachments[]')

        if not all([title, description, assignee_ids, due_date, project_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('tasks:tasks_assigned_by_me')

        try:
            project = Project.objects.get(id=project_id)

            # Create the base task
            task = Task.objects.create(
                project=project,
                title=title,
                description=description,
                creator=request.user,
                due_date=due_date
            )

            # Handle multiple assignees
            assigned_users = []
            for assignee_id in assignee_ids:
                try:
                    assignee = CustomUser.objects.get(id=assignee_id)
                    # Create a copy of the task for each assignee
                    if len(assignee_ids) > 1:
                        assignee_task = Task.objects.create(
                            project=project,
                            title=f"{title} (Assigned to {assignee.get_full_name() or assignee.username})",
                            description=description,
                            assignee=assignee,
                            creator=request.user,
                            due_date=due_date,
                            parent_task=task
                        )
                    else:
                        task.assignee = assignee
                        task.save()
                    assigned_users.append(assignee.get_full_name() or assignee.username)
                except CustomUser.DoesNotExist:
                    messages.warning(request, f'User with ID {assignee_id} not found.')

            # Handle file attachments using Document model
            for file in files:
                if file.size <= 10 * 1024 * 1024:  # 10MB limit
                    Document.objects.create(
                        title=file.name,
                        file=file,
                        content_type=ContentType.objects.get_for_model(task),
                        object_id=task.id,
                        uploaded_by=request.user
                    )
                else:
                    messages.warning(request, f'File {file.name} exceeds 10MB limit and was not uploaded.')

            # Success message
            assignee_list = ", ".join(assigned_users)
            attachment_count = len([f for f in files if f.size <= 10 * 1024 * 1024])
            messages.success(
                request,
                f'Task "{title}" has been successfully assigned to {assignee_list}. '
                f'Due date: {task.due_date.strftime("%B %d, %Y")}. '
                f'{attachment_count} file(s) attached.'
            )

        except ValueError as ve:
            messages.error(request, f'Invalid data provided: {str(ve)}')
        except Exception as e:
            messages.error(request, f'Error assigning task: {str(e)}')

    return redirect('tasks:tasks_assigned_by_me')