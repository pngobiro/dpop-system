# apps/meetings/views/lists.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from apps.meetings.models import Meeting
from apps.organization.models import Department
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def meeting_list(request):
    """View for listing meetings based on user's role and department"""
    user = request.user
    today = timezone.now().date()
    thirty_days_ago = today - timezone.timedelta(days=30)
    thirty_days_ahead = today + timezone.timedelta(days=30)

    # Base query for user's meetings
    base_query = Q(department=user.department) | Q(participants=user)

    # Get upcoming meetings (excluding today)
    upcoming_meetings = list(Meeting.objects.filter(
        date__gt=today,
        date__lte=thirty_days_ahead,
        status='scheduled'
    ).filter(base_query).distinct().order_by('date', 'start_time')[:5])

    # Get recent meetings
    recent_meetings = list(Meeting.objects.filter(
        date__lt=today,
        date__gte=thirty_days_ago
    ).filter(base_query).distinct().order_by('-date')[:5])

    # Get my meetings
    my_meetings = list(Meeting.objects.filter(
        Q(organizer=user) | Q(participants=user)
    ).distinct().order_by('date')[:5])

    # Filter out any meetings with invalid or null PKs
    upcoming_meetings = [m for m in upcoming_meetings if m and m.pk]
    recent_meetings = [m for m in recent_meetings if m and m.pk]
    my_meetings = [m for m in my_meetings if m and m.pk]
    
    # Check if user can view all meetings
    can_view_all = user.has_perm('meetings.view_all_meetings')
    
    if can_view_all:
        meetings = Meeting.objects.all()
    else:
        # Department users see only their department meetings
        meetings = Meeting.objects.filter(base_query).distinct()

    # Filter options
    status = request.GET.get('status')
    meeting_type = request.GET.get('meeting_type')
    department_id = request.GET.get('department')

    if status:
        meetings = meetings.filter(status=status)
    if meeting_type:
        meetings = meetings.filter(meeting_type=meeting_type)
    if department_id and can_view_all:
        meetings = meetings.filter(department_id=department_id)

    # Get meeting type and mode statistics
    type_query = meetings
    if not can_view_all:
        type_query = type_query.filter(base_query)
    
    meetings_by_type = list(type_query.values('meeting_type__name')
                          .annotate(count=Count('id'))
                          .values('meeting_type', 'count'))

    meetings_by_mode = list(type_query.values('meeting_mode')
                          .annotate(count=Count('id'))
                          .values('meeting_mode', 'count'))

    # Pagination
    paginator = Paginator(meetings.order_by('-date'), 10)
    page = request.GET.get('page')
    meetings = paginator.get_page(page)

    # Calculate statistics
    stats = {
        'total_meetings': Meeting.objects.filter(base_query).distinct().count(),
        'upcoming_count': Meeting.objects.filter(
            date__gte=today,
            status='scheduled'
        ).filter(base_query).distinct().count(),
        'completed_count': Meeting.objects.filter(
            status='completed',
            date__gte=thirty_days_ago
        ).filter(base_query).distinct().count(),
        'cancelled_count': Meeting.objects.filter(
            status='cancelled',
            date__gte=thirty_days_ago
        ).filter(base_query).distinct().count(),
    }

    context = {
        'meetings': meetings,
        'departments': Department.objects.all() if can_view_all else None,
        'can_view_all': can_view_all,
        'upcoming_meetings': upcoming_meetings,
        'recent_meetings': recent_meetings,
        'my_meetings': my_meetings,
        'meetings_by_type': meetings_by_type,
        'meetings_by_mode': meetings_by_mode,
        'stats': stats,
    }
    return render(request, 'meetings/meeting_list.html', context)