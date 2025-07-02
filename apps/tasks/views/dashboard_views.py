"""
Dashboard views for task management system.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.tasks.models import Task, Project
from apps.meetings.models import Meeting
from apps.document_management.models import Document
from apps.memos.models import Memo
from apps.tasks.utils.statistics import get_task_statistics


@login_required
def user_tasks_dashboard(request):
    """Dashboard showing user's tasks"""
    today = timezone.now().date()
    
    # Get tasks assigned to the user
    assigned_tasks = Task.objects.filter(assignees=request.user).select_related('project').prefetch_related('assignees').order_by('due_date')
    
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
    my_tasks_queryset = Task.objects.filter(assignees=request.user)
    my_tasks_stats = get_task_statistics(my_tasks_queryset)
    
    # Get tasks I assigned to others
    tasks_i_assigned_queryset = Task.objects.filter(creator=request.user)
    assigned_tasks_stats = get_task_statistics(tasks_i_assigned_queryset)
    
    # Get meetings stats
    all_meetings = Meeting.objects.all()
    meetings_stats = {
        'upcoming': Meeting.objects.filter(date__gte=today).count(),
        'today': Meeting.objects.filter(date=today).count(),
        'this_week': Meeting.objects.filter(date__gte=today, date__lte=today + timezone.timedelta(days=7)).count()
    }
    
    # Get document count
    document_count = Document.objects.count() if Document else 0

    # Get memos created by the user
    my_memos = Memo.objects.filter(created_by=request.user).order_by('-created_at')[:5]

    # Get total memos for the user's department
    department_memos_count = Memo.objects.filter(department=request.user.department).count()
    
    context = {
        'my_tasks_stats': my_tasks_stats,
        'assigned_tasks_stats': assigned_tasks_stats,
        'meetings_stats': meetings_stats,
        'document_count': document_count,
        'my_memos': my_memos,
        'department_memos_count': department_memos_count,
        'segment': 'my_dashboard' # Add segment for active navigation
    }
    return render(request, 'tasks/my_dashboard.html', context)
