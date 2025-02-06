# apps/meetings/management/commands/seed_meetings.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.meetings.models import Meeting, MeetingParticipant
from apps.organization.models import Department
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds sample meetings for each department'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding meetings data...')

        # Get departments
        departments = Department.objects.all()
        try:
            director = User.objects.get(username='joseph.osewe')
        except User.DoesNotExist:
            self.stdout.write('Creating director user...')
            director = User.objects.create_user(
                username='joseph.osewe',
                email='joseph.osewe@judiciary.go.ke',
                first_name='Joseph',
                last_name='Osewe',
                is_staff=True,
                is_superuser=True
            )
            director.set_password('Admin123!')
            director.save()

        meeting_types = {
            'Department Internal': [
                'Monthly Performance Review',
                'Staff Meeting',
                'Team Building',
                'Strategy Session'
            ],
            'With Director': [
                'Quarterly Review',
                'Budget Planning',
                'Performance Assessment',
                'Strategic Planning'
            ],
            'Committee': [
                'Technical Committee',
                'Quality Assurance',
                'Research Committee',
                'Innovation Committee'
            ]
        }

        for department in departments:
            self.stdout.write(f'Creating meetings for {department.name}')
            
            # Get department head - first user in department with Assistant Director role
            dept_head = User.objects.filter(departments=department).first()
            
            if not dept_head:
                continue

            # Create meetings for each type
            for meeting_type, titles in meeting_types.items():
                for title in titles:
                    # Create future meeting
                    days_ahead = 14 if meeting_type == 'Department Internal' else 30
                    meeting_date = timezone.now().date() + timedelta(days=days_ahead)
                    
                    meeting = Meeting.objects.create(
                        title=f"{department.name} - {title}",
                        department=department,
                        meeting_type=meeting_type,
                        date=meeting_date,
                        start_time='10:00',
                        end_time='11:30',
                        meeting_mode='hybrid',
                        physical_location='Conference Room A',
                        virtual_platform='teams',
                        virtual_meeting_url='https://teams.microsoft.com/meeting',
                        agenda=f"""
                        1. Opening Remarks
                        2. Previous Action Items Review
                        3. {title} Main Agenda
                        4. Department Updates
                        5. Way Forward
                        6. AOB
                        """,
                        status='scheduled',
                        organizer=dept_head if meeting_type == 'Department Internal' else director
                    )

                    # Add participants
                    dept_staff = User.objects.filter(departments=department).distinct()

                    for staff in dept_staff:
                        MeetingParticipant.objects.create(
                            meeting=meeting,
                            participant=staff,
                            role='attendee'
                        )

                    # Add director for director meetings
                    if meeting_type == 'With Director':
                        MeetingParticipant.objects.create(
                            meeting=meeting,
                            participant=director,
                            role='organizer'
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded meetings data'))