# apps/meetings/views/base.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from apps.meetings.models import Meeting, MeetingParticipant, MeetingType
from apps.organization.models import Department
from authentication.models import CustomUser
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)
    week_end = today + timezone.timedelta(days=7)
    next_week_start = week_end + timezone.timedelta(days=1)
    next_week_end = next_week_start + timezone.timedelta(days=6)
    thirty_days_ago = today - timezone.timedelta(days=30)

    # Base query for user's meetings
    base_query = Q(department=user.department) | Q(participants=user) | Q(organizer=user)

    # Get today's meetings
    todays_meetings = Meeting.objects.filter(
        date=today
    ).filter(
        Q(status='scheduled') | Q(status='in_progress')
    ).filter(base_query).distinct().order_by('start_time')

    # Get tomorrow's meetings
    tomorrows_meetings = Meeting.objects.filter(
        date=tomorrow
    ).filter(
        Q(status='scheduled') | Q(status='in_progress')
    ).filter(base_query).distinct().order_by('start_time')

    # Get this week's meetings (excluding today and tomorrow)
    this_week_meetings = Meeting.objects.filter(
        date__gt=tomorrow,
        date__lte=week_end
    ).filter(
        Q(status='scheduled') | Q(status='in_progress')
    ).filter(base_query).distinct().order_by('date', 'start_time')

    # Get next week's meetings
    next_week_meetings = Meeting.objects.filter(
        date__gte=next_week_start,
        date__lte=next_week_end
    ).filter(
        Q(status='scheduled') | Q(status='in_progress')
    ).filter(base_query).distinct().order_by('date', 'start_time')

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
        'my_meetings_count': Meeting.objects.filter(
            Q(organizer=user) | Q(participants=user)
        ).distinct().count()
    }

    # Get data for new meeting modal
    meeting_types = MeetingType.objects.filter(is_active=True)
    # Get users in the same departments as the current user
    department_users = CustomUser.objects.filter(departments__in=user.departments.all(), is_active=True).distinct()

    current_date = timezone.now().date()
    
    context = {
        'stats': stats,
        'todays_meetings': todays_meetings,
        'tomorrows_meetings': tomorrows_meetings,
        'this_week_meetings': this_week_meetings,
        'next_week_meetings': next_week_meetings,
        'meeting_types': meeting_types,
        'department_users': department_users,
        'current_date': current_date
    }
    return render(request, 'meetings/dashboard.html', context)

@login_required
def director_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied")
        return redirect('meetings:dashboard')

    today = timezone.now().date()
    departments = Department.objects.all()
    dept_meetings = {}

    for dept in departments:
        dept_meetings[dept] = {
            'upcoming': Meeting.objects.filter(
                department=dept,
                date__gte=today,
                status='scheduled'
            ).order_by('date')[:5],
            'recent': Meeting.objects.filter(
                department=dept,
                date__lt=today
            ).order_by('-date')[:5],
            'stats': {
                'total': Meeting.objects.filter(department=dept).count(),
                'scheduled': Meeting.objects.filter(
                    department=dept, 
                    status='scheduled'
                ).count(),
                'completed': Meeting.objects.filter(
                    department=dept,
                    status='completed'
                ).count()
            }
        }

    context = {
        'dept_meetings': dept_meetings,
        'total_meetings': Meeting.objects.count(),
        'total_participants': MeetingParticipant.objects.count()
    }
    
    return render(request, 'meetings/director_dashboard.html', context)