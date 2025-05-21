from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.tasks.models import Task
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
    
    # Get document count
    document_count = Document.objects.count()
    
    context = {
        'my_tasks_stats': my_tasks_stats,
        'assigned_tasks_stats': assigned_tasks_stats,
        'meetings_stats': meetings_stats,
        'document_count': document_count
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

    context = {
        'tasks': tasks,
        'title': 'Tasks I Assigned'
    }
    return render(request, 'tasks/tasks_assigned.html', context)