"""
Task statistics utilities for calculating task metrics and counts.
"""
from apps.tasks.models import Task


def get_task_statistics(task_queryset):
    """
    Calculates and returns a dictionary of task statistics for a given queryset.
    
    Args:
        task_queryset: QuerySet of Task objects
        
    Returns:
        dict: Dictionary containing counts for each task status
    """
    stats = {
        'total': task_queryset.count(),
        'TODO': task_queryset.filter(status=Task.StatusChoices.TODO).count(),
        'IN_PROGRESS': task_queryset.filter(status=Task.StatusChoices.IN_PROGRESS).count(),
        'DONE': task_queryset.filter(status=Task.StatusChoices.DONE).count(),
        'BLOCKED': task_queryset.filter(status=Task.StatusChoices.BLOCKED).count(),
        'APPROVED': task_queryset.filter(status=Task.StatusChoices.APPROVED).count(),
        'REJECTED': task_queryset.filter(status=Task.StatusChoices.REJECTED).count(),
        'IN_REVIEW': task_queryset.filter(status=Task.StatusChoices.IN_REVIEW).count(),
        'ON_HOLD': task_queryset.filter(status=Task.StatusChoices.ON_HOLD).count(),
    }
    return stats
