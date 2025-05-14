# apps/meetings/views/calendar.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from calendar import monthcalendar
import calendar
from datetime import datetime, date, timedelta
from ..models import Meeting, MeetingType
from apps.organization.models import Department
from apps.statistics.models import FinancialYear, FinancialQuarter
from django.utils.safestring import mark_safe
from itertools import chain

class Calendar:
    def __init__(self, year=None, month=None):
        self.year = year or timezone.now().year
        self.month = month or timezone.now().month
        
    def formatday(self, day, meetings):
        """Format a day with its meetings."""
        meetings_per_day = meetings.filter(date__day=day)
        d = ''
        for meeting in meetings_per_day:
            badge_class = ''
            if meeting.meeting_type == 'director':
                badge_class = 'text-danger'
            elif meeting.meeting_type == 'department':
                badge_class = 'text-primary'
            elif meeting.meeting_type == 'committee':
                badge_class = 'text-success'
                
            d += f'''<div class="mb-2">
                <a href="/meetings/{meeting.pk}/" 
                   class="text-decoration-none {badge_class}">
                    <small class="fw-bold">{meeting.start_time.strftime('%H:%M')}</small> - {meeting.title[:30]}...
                </a>
            </div>'''
            
        if day != 0:
            today = timezone.localtime().date()
            today_class = 'table-primary' if today == date(self.year, self.month, day) else ''
            current_date = date(self.year, self.month, day)
            return f"""
                <td class="align-top p-3 {today_class}" style="height: 180px; min-width: 200px;">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="fs-4 fw-bold">{day}</div>
                        <button type="button"
                                class="btn btn-sm btn-outline-primary quick-add-meeting"
                                data-date="{current_date}"
                                data-bs-toggle="modal"
                                data-bs-target="#addMeetingModal">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    <div class="overflow-hidden">{d}</div>
                </td>
            """
        return '<td class="bg-light"></td>'

    def formatweek(self, week, meetings):
        """Format a complete week."""
        week_days = ''
        for day in week:
            week_days += self.formatday(day, meetings)
        return f'<tr>{week_days}</tr>'

    def formatmonth(self, meetings):
        """Format the entire month."""
        cal = monthcalendar(self.year, self.month)
        
        month_header = f'''
        <thead>
            <tr>
                <th colspan="7" class="bg-primary text-white text-center p-4 fs-3">
                    {calendar.month_name[self.month]} {self.year}
                </th>
            </tr>
            <tr>
                <th class="text-center p-3 fs-5">Mon</th>
                <th class="text-center p-3 fs-5">Tue</th>
                <th class="text-center p-3 fs-5">Wed</th>
                <th class="text-center p-3 fs-5">Thu</th>
                <th class="text-center p-3 fs-5">Fri</th>
                <th class="text-center p-3 fs-5">Sat</th>
                <th class="text-center p-3 fs-5">Sun</th>
            </tr>
        </thead>
        '''
        
        weeks = ''
        for week in cal:
            weeks += self.formatweek(week, meetings)
            
        return mark_safe(f'<table class="table table-bordered table-lg mb-0">{month_header}<tbody>{weeks}</tbody></table>')

@login_required
def calendar_view(request):
    """View for displaying the calendar with meetings."""
    
    # Get current date with timezone awareness
    current_date = timezone.localtime().date()
    
    # Get current financial year
    current_fy = FinancialYear.objects.filter(
        start_date__date__lte=current_date,
        end_date__date__gte=current_date
    ).first()
    
    # Get default quarter
    if current_fy:
        current_quarter = FinancialQuarter.objects.filter(
            financial_year=current_fy,
            start_date__lte=current_date,
            end_date__gte=current_date
        ).first()
        default_quarter = str(current_quarter.quarter_number) if current_quarter else None
    else:
        default_quarter = None
        
    selected_quarter = request.GET.get('quarter', default_quarter)
    
    # Get selected month and year
    if selected_quarter and not request.GET.get('month') and current_fy:
        try:
            quarter = FinancialQuarter.objects.get(
                financial_year=current_fy,
                quarter_number=int(selected_quarter)
            )
            month = quarter.start_date.month
            year = quarter.start_date.year
        except (FinancialQuarter.DoesNotExist, ValueError):
            month = current_date.month
            year = current_date.year
    else:
        month = int(request.GET.get('month', current_date.month))
        year = int(request.GET.get('year', current_date.year))
    
    department_id = request.GET.get('department')
    
    # Filter meetings based on permissions
    user = request.user
    if user.has_perm('meetings.view_all_meetings'):
        meetings = Meeting.objects.all()
    else:
        meetings = Meeting.objects.filter(
            Q(department=user.department) | Q(participants=user)
        ).distinct()
    
    # Apply department filter if user has permission
    if department_id and user.has_perm('meetings.view_all_meetings'):
        meetings = meetings.filter(department_id=department_id)
    
    # Apply quarter filter
    if selected_quarter and current_fy:
        try:
            quarter = FinancialQuarter.objects.get(
                financial_year=current_fy,
                quarter_number=int(selected_quarter)
            )
            meetings = meetings.filter(
                date__range=[quarter.start_date, quarter.end_date]
            )
        except (FinancialQuarter.DoesNotExist, ValueError):
            pass
    
    # Filter for selected month
    meetings = meetings.filter(date__year=year, date__month=month)
    
    # Navigation links
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    # Create calendar
    cal = Calendar(year, month)
    calendar_html = cal.formatmonth(meetings)
    
    # Get departments for filter (if user has permission)
    departments = None
    if user.has_perm('meetings.view_all_meetings'):
        departments = Department.objects.all()
    
    # Get quarters for current financial year
    quarters = []
    if current_fy:
        quarters = [
            (str(q.quarter_number), 
             f'Quarter {q.quarter_number} ({q.start_date.strftime("%b")} - {q.end_date.strftime("%b")})')
            for q in FinancialQuarter.objects.filter(financial_year=current_fy).order_by('quarter_number')
        ]
    
    # Get meeting types from database
    meeting_types = [{'value': mt.id, 'display': mt.name}
                    for mt in MeetingType.objects.filter(is_active=True)]
    
    context = {
        'calendar': calendar_html,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'current_month': calendar.month_name[month],
        'current_year': year,
        'departments': departments,
        'selected_department': department_id,
        'quarters': quarters,
        'selected_quarter': selected_quarter,
        'current_fy': current_fy,
        'meeting_types': meeting_types,
    }
    
    return render(request, 'meetings/calendar.html', context)