# apps/mail/models.py
from django.db import models 
from django.conf import settings
from apps.document_management.models import Document
from apps.organization.models import Department
from django.utils import timezone

class PhysicalMail(models.Model):
    MAIL_TYPE_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    
    MAIL_STATUS_CHOICES = [
        ('received', 'Received at Registry'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('pending_dispatch', 'Pending Dispatch'),
        ('dispatched', 'Dispatched'),
        ('acknowledged', 'Acknowledgment Received'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('express', 'Express'),
        ('urgent', 'Urgent'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('hand_delivery', 'Hand Delivery'),
        ('postal', 'Postal Service'),
        ('courier', 'Courier Service'),
        ('diplomatic_bag', 'Diplomatic Bag'),
    ]

    # Basic Information
    tracking_number = models.CharField(max_length=100, unique=True)
    mail_type = models.CharField(max_length=20, choices=MAIL_TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    description = models.TextField(help_text="Brief description of mail contents")
    date_received = models.DateTimeField(null=True, blank=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    
    # Classification and Routing
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='physical_mails')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    confidential = models.BooleanField(default=False)
    file_number = models.CharField(max_length=100, help_text="Physical file reference number")
    
    # Physical Mail Specific
    delivery_method = models.CharField(max_length=50, choices=DELIVERY_METHOD_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight in grams")
    postage_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    courier_name = models.CharField(max_length=100, blank=True)
    courier_tracking_number = models.CharField(max_length=100, blank=True)
    
    # Metadata
    status = models.CharField(max_length=20, choices=MAIL_STATUS_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_physical_mails'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # External Party Information
    sender_name = models.CharField(max_length=255)
    sender_address = models.TextField()
    sender_phone = models.CharField(max_length=50, blank=True)
    
    recipient_name = models.CharField(max_length=255)
    recipient_address = models.TextField()
    recipient_phone = models.CharField(max_length=50, blank=True)
    
    # Response Tracking
    requires_response = models.BooleanField(default=False)
    response_deadline = models.DateField(null=True, blank=True)
    response_mail = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='original_mail'
    )

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_mark_confidential", "Can mark mail as confidential"),
            ("view_confidential_mail", "Can view confidential mail"),
            ("process_incoming_mail", "Can process incoming mail"),
            ("dispatch_outgoing_mail", "Can dispatch outgoing mail"),
        ]

    def __str__(self):
        return f"{self.tracking_number} - {self.subject}"

class MailAttachment(models.Model):
    """Physical attachments to mail"""
    mail = models.ForeignKey(PhysicalMail, on_delete=models.CASCADE, related_name='attachments')
    name = models.CharField(max_length=255)
    description = models.TextField()
    attachment_type = models.CharField(max_length=100, help_text="Type of physical attachment")
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=100, help_text="Condition of the attachment")
    
    # If there's a digital copy
    digital_copy = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='physical_attachments'
    )
    
    class Meta:
        ordering = ['name']

class MailMovement(models.Model):
    """Track physical movement of mail"""
    mail = models.ForeignKey(PhysicalMail, on_delete=models.CASCADE, related_name='movements')
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    received_by = models.CharField(max_length=255, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

class MailActivity(models.Model):
    """Track all mail-related activities"""
    ACTION_CHOICES = [
        ('receive', 'Received at Registry'),
        ('register', 'Registered'),
        ('assign', 'Assigned'),
        ('forward', 'Forwarded'),
        ('process', 'Processed'),
        ('dispatch', 'Dispatched'),
        ('deliver', 'Delivered'),
        ('archive', 'Archived'),
    ]

    mail = models.ForeignKey(PhysicalMail, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, help_text="Physical location where activity occurred")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Mail Activities'

class MailAssignment(models.Model):
    """Track mail assignments to users"""
    mail = models.ForeignKey(PhysicalMail, on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_mails'
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mail_assignments_given'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Physical handling
    current_location = models.CharField(max_length=255, help_text="Current physical location of the mail")
    acknowledgment_required = models.BooleanField(default=True)
    acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-assigned_at']

# utils.py functions for tracking number generation
def generate_tracking_number():
    """Generate a unique tracking number for physical mail"""
    year = timezone.now().year
    month = timezone.now().month
    # Get count of mail for current month
    count = PhysicalMail.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).count() + 1
    return f"PM/{year}/{month:02d}/{count:04d}"