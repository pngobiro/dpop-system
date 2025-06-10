from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import redirect
from .models import Meeting, MeetingParticipant

@api_view(['GET', 'POST'])
def api_meeting_create(request):
    """Handle meeting creation - both form display and submission"""
    from django.shortcuts import render
    from apps.meetings.forms import MeetingForm
    
    if request.method == 'GET':
        form = MeetingForm(user=request.user)
        context = {
            'form': form,
            'action': 'Create'
        }
        return render(request, 'meetings/meeting_form.html', context)
    # Ensure user has a department
    if not request.user.department:
        return Response(
            {"error": "You must be assigned to a department to create meetings."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate required fields
    required_fields = ['title', 'meeting_type', 'date', 'start_time']
    missing_fields = [field for field in required_fields if not request.data.get(field)]
    if missing_fields:
        return Response(
            {"error": f"Missing required fields: {', '.join(missing_fields)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Create meeting with required fields
        meeting = Meeting.objects.create(
            title=request.data.get('title'),
            department=request.user.department,  # Department is automatically set from user's department
            meeting_type_id=request.data.get('meeting_type'),
            date=request.data.get('date'),
            start_time=request.data.get('start_time'),
            end_time=request.data.get('end_time'),
            meeting_mode=request.data.get('meeting_mode', 'physical'),
            physical_location=request.data.get('physical_location'),
            virtual_platform=request.data.get('virtual_platform'),
            virtual_meeting_url=request.data.get('virtual_meeting_url'),
            virtual_meeting_id=request.data.get('virtual_meeting_id'),
            virtual_meeting_password=request.data.get('virtual_meeting_password'),
            agenda=request.data.get('agenda', ''),
            organizer=request.user
        )

        # Add organizer as first participant
        MeetingParticipant.objects.create(
            meeting=meeting,
            participant=request.user,
            role='attendee'
        )

        # Return a redirect response to meetings dashboard
        from django.shortcuts import redirect
        return redirect('meetings:dashboard')

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )