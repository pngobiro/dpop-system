# apps/meetings/views/lists.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from apps.meetings.models import Meeting
from apps.organization.models import Department

@login_required
def meeting_list(request):
    """View for listing meetings based on user's role and department"""
    user = request.user
    
    # Check if user can view all meetings
    can_view_all = user.has_perm('meetings.view_all_meetings')
    
    if can_view_all:
        meetings = Meeting.objects.all()
    else:
        # Department users see only their department meetings
        meetings = Meeting.objects.filter(
            Q(department=user.department) | Q(participants=user)
        ).distinct()

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

    # Pagination
    paginator = Paginator(meetings.order_by('-date'), 10)
    page = request.GET.get('page')
    meetings = paginator.get_page(page)

    context = {
        'meetings': meetings,
        'departments': Department.objects.all() if can_view_all else None,
        'can_view_all': can_view_all,
    }
    return render(request, 'meetings/meeting_list.html', context)