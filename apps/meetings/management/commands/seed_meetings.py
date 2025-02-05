# apps/meetings/management/commands/seed_meetings.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from apps.meetings.models import Meeting, MeetingParticipant, MeetingDocument
from apps.organization.models import Department
from datetime import timedelta, datetime

class Command(BaseCommand):
    help = 'Seeds meetings data'

    def create_default_users(self):
        """Create default users if they don't exist."""
        director, created = User.objects.get_or_create(
            username='director',
            defaults={
                'email': 'director@judiciary.go.ke',
                'first_name': 'John',
                'last_name': 'Director',
                'is_staff': True
            }
        )
        if created:
            director.set_password('director123')  # Set a default password
            director.save()
            self.stdout.write(self.style.SUCCESS('Created director user'))
        return director

    def handle(self, *args, **options):
        self.stdout.write('Seeding meetings data...')

        try:
            # Ensure we have a director user
            director = self.create_default_users()

            # Get departments
            departments = Department.objects.all()
            if not departments.exists():
                self.stdout.write(self.style.WARNING('No departments found. Please run seed_organization first.'))
                return

            # Sample meeting data
            meetings_data = [
                {
                    'title': 'Performance Management Review',
                    'meeting_type': 'director',
                    'meeting_mode': 'hybrid',
                    'physical_location': 'Conference Room A',
                    'virtual_platform': 'zoom',
                    'virtual_meeting_url': 'https://zoom.us/j/example',
                    'virtual_meeting_id': '123456789',
                    'virtual_meeting_password': 'performance',
                    'agenda': '''
                    1. Review of Q1 Performance Metrics
                    2. Discussion of KPIs
                    3. Planning for Q2
                    4. AOB
                    ''',
                    'status': 'scheduled'
                },
                {
                    'title': 'Budget Planning Session',
                    'meeting_type': 'department',
                    'meeting_mode': 'virtual',
                    'virtual_platform': 'teams',
                    'virtual_meeting_url': 'https://teams.microsoft.com/l/example',
                    'virtual_meeting_id': '987654321',
                    'virtual_meeting_password': 'budget2025',
                    'agenda': '''
                    1. Budget Review 2024
                    2. Budget Allocation 2025
                    3. Cost Saving Measures
                    4. Project Funding Requirements
                    ''',
                    'status': 'scheduled'
                },
                {
                    'title': 'Data Quality Workshop',
                    'meeting_type': 'committee',
                    'meeting_mode': 'physical',
                    'physical_location': 'Training Room B',
                    'agenda': '''
                    1. Current Data Quality Issues
                    2. Data Collection Standards
                    3. Quality Improvement Measures
                    4. Training Requirements
                    ''',
                    'status': 'scheduled'
                }
            ]

            # Create meetings for each department
            for dept in departments:
                for idx, meeting_data in enumerate(meetings_data):
                    # Calculate meeting date (future dates)
                    meeting_date = timezone.now().date() + timedelta(days=idx+1)

                    # Create meeting
                    meeting = Meeting.objects.create(
                        title=f"{dept.name} - {meeting_data['title']}",
                        department=dept,
                        meeting_type=meeting_data['meeting_type'],
                        meeting_mode=meeting_data['meeting_mode'],
                        date=meeting_date,
                        start_time=datetime.strptime('10:00', '%H:%M').time(),
                        end_time=datetime.strptime('11:30', '%H:%M').time(),
                        physical_location=meeting_data.get('physical_location', ''),
                        virtual_platform=meeting_data.get('virtual_platform', ''),
                        virtual_meeting_url=meeting_data.get('virtual_meeting_url', ''),
                        virtual_meeting_id=meeting_data.get('virtual_meeting_id', ''),
                        virtual_meeting_password=meeting_data.get('virtual_meeting_password', ''),
                        agenda=meeting_data['agenda'],
                        status=meeting_data['status'],
                        organizer=director
                    )

                    # Create a participant entry for the organizer
                    MeetingParticipant.objects.create(
                        meeting=meeting,
                        participant=director,
                        role='organizer',
                    )

                    self.stdout.write(self.style.SUCCESS(
                        f'Created meeting: {meeting.title}'
                    ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding meetings: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded meetings data'))