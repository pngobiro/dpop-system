# apps/meetings/models.py
from django.db import models
from django.conf import settings
from apps.organization.models import Department
from apps.document_management.models import Document


class MeetingAction(models.Model):
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    due_date = models.DateField()

    class Meta:
        verbose_name = 'Meeting Action Item'
        verbose_name_plural = 'Meeting Action Items'

    def __str__(self):
        return f"{self.description} - {self.meeting.title}"
    
    

class MeetingDocument(models.Model):
    DOCUMENT_TYPES = [
        ('agenda', 'Agenda'),
        ('minutes', 'Minutes'),
        ('presentation', 'Presentation'),
        ('report', 'Report'),
        ('other', 'Other')
    ]

    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    notes = models.TextField(blank=True, help_text="Additional notes about the document")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['meeting', 'document']
        verbose_name = 'Meeting Document'
        verbose_name_plural = 'Meeting Documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.meeting}"



class MeetingParticipant(models.Model):
    PARTICIPANT_ROLE = [
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
        ('guest', 'Guest')
    ]

    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=PARTICIPANT_ROLE, default='attendee')

    class Meta:
        unique_together = ['meeting', 'participant']
        verbose_name = 'Meeting Participant'
        verbose_name_plural = 'Meeting Participants'

    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.get_role_display()}"
    
    

class Meeting(models.Model):
    MEETING_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    MEETING_TYPE = [
        ('department', 'Department Internal'),
        ('director', 'With Director'),
        ('committee', 'Committee Meeting'),
        ('other', 'Other')
    ]
    
    MEETING_MODE = [
        ('physical', 'Physical'),
        ('virtual', 'Virtual'),
        ('hybrid', 'Hybrid')
    ]

    # Basic Info
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='meetings')
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Location/Mode
    meeting_mode = models.CharField(max_length=20, choices=MEETING_MODE, default='physical')
    physical_location = models.CharField(max_length=255, blank=True, null=True)
    virtual_meeting_url = models.URLField(blank=True, null=True)
    virtual_meeting_id = models.CharField(max_length=100, blank=True, null=True, help_text="Meeting ID for virtual platform")
    virtual_meeting_password = models.CharField(max_length=50, blank=True, null=True, help_text="Password for virtual meeting")
    virtual_platform = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        choices=[
            ('zoom', 'Zoom'),
            ('teams', 'Microsoft Teams'),
            ('meet', 'Google Meet'),
            ('other', 'Other Platform')
        ]
    )

    # Content
    agenda = models.TextField()
    minutes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=MEETING_STATUS, default='scheduled')
    
    # Meeting organization
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_meetings')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='MeetingParticipant', related_name='meetings')
    
    # Recording (for virtual meetings)
    recording_url = models.URLField(blank=True, null=True)
    has_recording = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']
        permissions = [
            ("view_all_meetings", "Can view all meetings across departments"),
            ("manage_department_meetings", "Can manage department meetings"),
        ]

    def __str__(self):
        return f"{self.title} - {self.department.name} ({self.date})"
    
    def get_meeting_location(self):
        """Returns formatted meeting location/link based on meeting mode"""
        if self.meeting_mode == 'physical':
            return self.physical_location
        elif self.meeting_mode == 'virtual':
            return self.virtual_meeting_url
        else:  # hybrid
            return f"Physical: {self.physical_location}\nVirtual: {self.virtual_meeting_url}"

    def get_meeting_access_info(self):
        """Returns formatted virtual meeting access information"""
        if self.meeting_mode in ['virtual', 'hybrid']:
            info = []
            if self.virtual_platform:
                info.append(f"Platform: {self.get_virtual_platform_display()}")
            if self.virtual_meeting_url:
                info.append(f"URL: {self.virtual_meeting_url}")
            if self.virtual_meeting_id:
                info.append(f"Meeting ID: {self.virtual_meeting_id}")
            if self.virtual_meeting_password:
                info.append(f"Password: {self.virtual_meeting_password}")
            return "\n".join(info)
        return ""