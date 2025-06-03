# apps/meetings/views/calendar.py
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from calendar import monthcalendar # Used by your Calendar class
import calendar # Python's standard calendar module
from datetime import datetime, date, timedelta # datetime not directly used, date and timedelta might be
from ..models import Meeting, MeetingType
from apps.organization.models import Department
from apps.statistics.models import FinancialYear, FinancialQuarter
from django.utils.safestring import mark_safe
# from itertools import chain # Not used in the provided snippet

logger = logging.getLogger(__name__)

class Calendar:
    def __init__(self, year=None, month=None):
        # These will be the year/month the calendar intends to display
        self.year = year if year is not None else timezone.now().year
        self.month = month if month is not None else timezone.now().month
        
    def formatday(self, day, meetings):
        """Format a day with its meetings."""
        meetings_per_day = meetings.filter(date__day=day)
        d = ''
        for meeting in meetings_per_day:
            # Map meeting types to badge classes
            badge_class = ''
            type_name = meeting.meeting_type.name.lower()
            if 'director' in type_name:
                badge_class = 'text-danger'
            elif 'department' in type_name:
                badge_class = 'text-primary'
            elif 'committee' in type_name:
                badge_class = 'text-success'
                
            d += f'<div class="mb-1">' # Reduced margin for more items
            # Ensure this URL is appropriate for the quick view modal (might need an AJAX endpoint)
            d += f'<a href="/meetings/{meeting.pk}/" class="text-decoration-none {badge_class} meeting-link" title="{meeting.title}">'
            d += f'<small class="fw-bold">{meeting.start_time.strftime("%H:%M") if meeting.start_time else ""}</small> - {meeting.title[:25]}{"..." if len(meeting.title) > 25 else ""}'
            d += '</a>'
            d += '</div>'
            
        if day != 0:
            current_processing_date = date(self.year, self.month, day)
            today_class = 'table-info' if timezone.localtime().date() == current_processing_date else '' # Bootstrap's 'table-info' for highlight

            return f"""
                <td class="align-top p-2 {today_class}" style="height: 150px; min-width: 180px; vertical-align: top;">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <div class="fs-5 fw-bold">{day}</div>
                        <button type="button"
                                class="btn btn-xs btn-outline-primary quick-add-meeting"
                                data-date="{current_processing_date.isoformat()}"
                                title="Add meeting on {current_processing_date.strftime('%d-%m-%Y')}">
                            <i class="fas fa-plus"></i> Add
                        </button>
                    </div>
                    <div class="overflow-auto" style="max-height: 100px;">{d if d else '<small class="text-muted">No meetings</small>'}</div>
                </td>
            """
        return '<td class="noday bg-light"> </td>' # Added noday class and BG for clarity

    def formatweek(self, week, meetings):
        """Format a complete week."""
        week_days = ''
        for day_tuple in week: # monthcalendar returns tuples (day, weekday) if used directly
                              # your current code passes week as list of day numbers
            day_number = day_tuple[0] if isinstance(day_tuple, tuple) else day_tuple
            week_days += self.formatday(day_number, meetings)
        return f'<tr>{week_days}</tr>'

    def formatmonth(self, meetings):
        """Format the entire month."""
        # monthcalendar from calendar module gives weeks starting Monday
        cal_weeks = monthcalendar(self.year, self.month) 
        
        month_header = f'''
        <thead>
            <tr>
                <th colspan="7" class="bg-primary text-white text-center p-3 fs-4">
                    {calendar.month_name[self.month]} {self.year}
                </th>
            </tr>
            <tr>
                {''.join(f'<th class="text-center p-2 small text-muted">{calendar.day_abbr[i]}</th>' for i in range(7))}
            </tr>
        </thead>
        '''
        
        weeks_html = ''
        for week in cal_weeks: # week is a list of day numbers (0 for days outside month)
            weeks_html += self.formatweek(week, meetings) # Pass the list of day numbers
            
        return mark_safe(f'<table class="table table-bordered table-calendar mb-0">{month_header}<tbody>{weeks_html}</tbody></table>')

@login_required
def calendar_view(request):
    logger.info(f"Calendar view accessed by user: {request.user.username}")
    
    current_system_date = timezone.localtime().date()
    logger.debug(f"Current system date: {current_system_date}")

    # --- Determine Year and Month for Calendar Display ---
    # Default to current system month/year if not specified in GET parameters
    year_to_display = int(request.GET.get('year', current_system_date.year))
    month_to_display = int(request.GET.get('month', current_system_date.month))
    
    # Validate month
    if not (1 <= month_to_display <= 12):
        month_to_display = current_system_date.month
        year_to_display = current_system_date.year # Reset year if month was invalid
    logger.debug(f"Calendar will display: Month {month_to_display}, Year {year_to_display}")

    # --- Financial Year and Quarter Logic ---
    date_being_displayed = date(year_to_display, month_to_display, 1) # 1st day of the month being displayed

    # FY for the "Financial Year: X" header (based on current system date)
    fy_for_header = FinancialYear.objects.filter(
        start_date__date__lte=current_system_date,
        end_date__date__gte=current_system_date
    ).first()

    # FY relevant to the date actually being displayed on the calendar
    fy_of_displayed_date = FinancialYear.objects.filter(
        start_date__date__lte=date_being_displayed,
        end_date__date__gte=date_being_displayed
    ).first()

    # Determine selected quarter value (string or None)
    # Priority: 1. GET param, 2. Quarter of the date_being_displayed (if its FY exists)
    selected_quarter_value = request.GET.get('quarter') 
    if selected_quarter_value is None and fy_of_displayed_date:
        quarter_obj_for_displayed_date = FinancialQuarter.objects.filter(
            financial_year=fy_of_displayed_date,
            start_date__lte=date_being_displayed,
            end_date__gte=date_being_displayed
        ).first()
        if quarter_obj_for_displayed_date:
            selected_quarter_value = str(quarter_obj_for_displayed_date.quarter_number)
    
    logger.debug(f"Selected quarter value (for filtering/dropdown): {selected_quarter_value}")

    # Quarters list for the dropdown (based on the FY of the date being displayed)
    quarters_list_for_dropdown = []
    active_fy_for_dropdown = fy_of_displayed_date if fy_of_displayed_date else fy_for_header # Fallback to header's FY
    if active_fy_for_dropdown:
        quarters_list_for_dropdown = [
            (str(q.quarter_number), 
             f'Q{q.quarter_number} ({q.start_date.strftime("%b %d")} - {q.end_date.strftime("%b %d")})')
            for q in FinancialQuarter.objects.filter(financial_year=active_fy_for_dropdown).order_by('quarter_number')
        ]

    # --- Initialize and Filter Meetings Queryset ---
    meetings = Meeting.objects.select_related('department').prefetch_related('participants').all() # Optimization
    
    user = request.user
    can_view_all = user.has_perm('meetings.view_all_meetings')
    if not can_view_all:
        meetings = meetings.filter(
            Q(department=user.department) | Q(participants=user)
        ).distinct()

    department_id = request.GET.get('department')
    if department_id: # Apply department filter if selected
        if can_view_all or (user.department and str(user.department.id) == department_id):
            meetings = meetings.filter(department_id=department_id)
        # else: user trying to filter by department they don't have access to (if not can_view_all) - implicitly handled by prior permission filter.

    # Apply Quarter Filter (if a quarter is selected and its FY context is known)
    if selected_quarter_value and active_fy_for_dropdown: # Use the same FY as the dropdown list
        try:
            quarter_to_filter_by = FinancialQuarter.objects.get(
                financial_year=active_fy_for_dropdown, 
                quarter_number=int(selected_quarter_value)
            )
            meetings = meetings.filter(
                date__gte=quarter_to_filter_by.start_date,
                date__lte=quarter_to_filter_by.end_date 
            )
            logger.debug(f"Meetings filtered by Quarter {selected_quarter_value} of FY {active_fy_for_dropdown.name}")
        except (FinancialQuarter.DoesNotExist, ValueError) as e:
            logger.warning(f"Could not apply quarter filter for Q{selected_quarter_value}, FY {active_fy_for_dropdown.name if active_fy_for_dropdown else 'Unknown'}: {e}")
    
    # Final filter for the specific month being displayed
    meetings = meetings.filter(date__year=year_to_display, date__month=month_to_display)
    logger.info(f"Found {meetings.count()} meetings for {calendar.month_name[month_to_display]} {year_to_display} (after all filters)")
    
    # --- Navigation links ---
    prev_month_nav = month_to_display - 1 if month_to_display > 1 else 12
    prev_year_nav = year_to_display if month_to_display > 1 else year_to_display - 1
    next_month_nav = month_to_display + 1 if month_to_display < 12 else 1
    next_year_nav = year_to_display if month_to_display < 12 else year_to_display + 1
    
    # --- Create Calendar HTML ---
    cal_instance = Calendar(year_to_display, month_to_display)
    calendar_html = cal_instance.formatmonth(meetings)
    
    # --- Prepare Context Data ---
    departments_for_filter = Department.objects.all() if can_view_all else None
    
    # Meeting types for the "Add Meeting" modal form
    # This matches your original template loop: {% for type in meeting_types %} ... {{ type.value }} ... {{ type.display }}
    meeting_types_for_form = []
    for mt in MeetingType.objects.filter(is_active=True).order_by('name'):
        meeting_types_for_form.append({
            'value': mt.id, # Assuming mt.id is the value you want for the option
            'display': mt.name
        })
    
    context = {
        'calendar': calendar_html,
        'prev_month': prev_month_nav,
        'prev_year': prev_year_nav,
        'next_month': next_month_nav,
        'next_year': next_year_nav,
        'current_month_name': calendar.month_name[month_to_display],
        'current_year_value': year_to_display,
        'departments': departments_for_filter,
        'selected_department': department_id, # This is the string from GET or None
        'quarters': quarters_list_for_dropdown,
        'selected_quarter': selected_quarter_value, # This is the string from GET/default or None
        'current_fy': fy_for_header, # For the "Financial Year: X" display
        'meeting_types': meeting_types_for_form,
    }
    
    return render(request, 'meetings/calendar.html', context)