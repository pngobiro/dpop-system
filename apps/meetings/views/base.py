# apps/meetings/views/base.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from apps.meetings.models import Meeting, MeetingParticipant
from apps.organization.models import Department

@login_required 
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    thirty_days_ago = today - timezone.timedelta(days=30)

    base_query = Q(department=user.department) | Q(participants=user)

    stats = {
        'total_meetings': Meeting.objects.filter(base_query).distinct().count(),
        'upcoming_count': Meeting.objects.filter(
            date__gte=today,
            status='scheduled'
        ).filter(base_query).distinct().count(),
        'completed_count': Meeting.objects.filter(
            status='completed',
            date__gte=thirty_days_ago
        ).filter(base_query).distinct().count()
    }

    upcoming_meetings = Meeting.objects.filter(
        date__gte=today,
        status='scheduled'
    ).filter(base_query).distinct().order_by('date', 'start_time')[:5]

    context = {
        'stats': stats,
        'upcoming_meetings': upcoming_meetings,
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