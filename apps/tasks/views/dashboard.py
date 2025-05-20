from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.tasks.models import Task

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