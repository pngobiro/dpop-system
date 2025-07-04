from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.organization.models import Department
from apps.document_management.models import Document, DocumentCategory
import uuid
import qrcode
from io import BytesIO
import base64


class MemoType(models.Model):
    """Types of memos in the system"""
    TYPE_CHOICES = [
        ('incoming', 'Incoming Memo'),
        ('outgoing', 'Outgoing Memo'),
        ('internal', 'Internal Memo'),
        ('external', 'External Memo'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    type_category = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MemoCategory(models.Model):
    """Categories for memo classification"""
    CATEGORY_CHOICES = [
        ('administrative', 'Administrative'),
        ('financial', 'Financial'),
        ('legal', 'Legal'),
        ('policy', 'Policy'),
        ('operational', 'Operational'),
        ('emergency', 'Emergency/Urgent'),
        ('routine', 'Routine'),
        ('hr', 'Human Resources'),
        ('procurement', 'Procurement'),
        ('strategic', 'Strategic'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color_code = models.CharField(max_length=7, default='#007bff', help_text="Hex color code for UI display")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Memo Categories"
    
    def __str__(self):
        return self.name


class PriorityLevel(models.Model):
    """Priority levels for memos"""
    PRIORITY_CHOICES = [
        ('emergency', 'Emergency'),
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    level = models.PositiveIntegerField(unique=True, help_text="1=Emergency, 5=Low")
    description = models.TextField(blank=True)
    color_code = models.CharField(max_length=7, default='#6c757d')
    response_time_hours = models.PositiveIntegerField(help_text="Expected response time in hours")
    escalation_time_hours = models.PositiveIntegerField(help_text="Time before escalation in hours")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['level']
    
    def __str__(self):
        return self.name


class MemoStatus(models.Model):
    """Status tracking for memo workflow"""
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('registered', 'Registered'),
        ('under_review', 'Under Review'),
        ('delegated', 'Delegated'),
        ('in_progress', 'In Progress'),
        ('pending_approval', 'Pending Approval'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('escalated', 'Escalated'),
        ('draft', 'Draft'),
        ('sent', 'Sent'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    status_type = models.CharField(max_length=20, choices=STATUS_CHOICES)
    color_code = models.CharField(max_length=7, default='#6c757d')
    is_final = models.BooleanField(default=False, help_text="Indicates if this is a final status")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Memo Statuses"
    
    def __str__(self):
        return self.name


class MemoWorkflow(models.Model):
    """Workflow definitions for different memo types"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    memo_type = models.ForeignKey(MemoType, on_delete=models.CASCADE, related_name='workflows')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.memo_type.name}"


class WorkflowStep(models.Model):
    """Individual steps in a workflow"""
    STEP_TYPES = [
        ('review', 'Review'),
        ('approve', 'Approve'),
        ('delegate', 'Delegate'),
        ('action', 'Action Required'),
        ('notify', 'Notify'),
        ('archive', 'Archive'),
    ]
    
    workflow = models.ForeignKey(MemoWorkflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    step_type = models.CharField(max_length=20, choices=STEP_TYPES)
    order = models.PositiveIntegerField()
    assigned_role = models.CharField(max_length=50, blank=True, help_text="Role required for this step")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    is_optional = models.BooleanField(default=False)
    time_limit_hours = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['workflow', 'order']
        unique_together = ['workflow', 'order']
    
    def __str__(self):
        return f"{self.workflow.name} - Step {self.order}: {self.name}"


class ActionItem(models.Model):
    """Trackable action items from memos"""
    ACTION_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]
    
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='action_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_actions')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delegated_actions')
    status = models.CharField(max_length=20, choices=ACTION_STATUS, default='pending')
    priority = models.ForeignKey(PriorityLevel, on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.assigned_to.get_full_name()}"


class Delegation(models.Model):
    """Track memo delegations"""
    DELEGATION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('escalated', 'Escalated'),
    ]
    
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='delegations')
    delegated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delegations_made')
    delegated_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delegations_received')
    status = models.CharField(max_length=20, choices=DELEGATION_STATUS, default='pending')
    instructions = models.TextField()
    due_date = models.DateTimeField()
    delegated_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-delegated_at']
    
    def __str__(self):
        return f"Delegation: {self.memo.subject} to {self.delegated_to.get_full_name()}"


class MemoDocument(models.Model):
    """Links memos to documents stored in Google Drive"""
    ATTACHMENT_TYPES = [
        ('scanned_original', 'Scanned Original Document'),
        ('supporting_doc', 'Supporting Document'),
        ('response_draft', 'Response Draft'),
        ('reference', 'Reference Material'),
        ('cover_letter', 'Cover Letter'),
        ('appendix', 'Appendix'),
        ('signature', 'Signature/Approval'),
        ('photo', 'Photo/Image'),
    ]
    
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='document_attachments')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=50, choices=ATTACHMENT_TYPES)
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False, help_text="Mark the main document")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['memo', 'document']
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.memo.subject} - {self.get_attachment_type_display()}"


class MemoTimeline(models.Model):
    """Timeline tracking for all memo events"""
    EVENT_TYPES = [
        ('created', 'Created'),
        ('received', 'Received'),
        ('registered', 'Registered'),
        ('assigned', 'Assigned'),
        ('delegated', 'Delegated'),
        ('status_changed', 'Status Changed'),
        ('commented', 'Commented'),
        ('document_added', 'Document Added'),
        ('document_removed', 'Document Removed'),
        ('escalated', 'Escalated'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='timeline_events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.memo.subject} - {self.get_event_type_display()}"


class ActionLog(models.Model):
    """Detailed action logging for audit purposes"""
    ACTION_TYPES = [
        ('create', 'Created'),
        ('read', 'Read'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('delegate', 'Delegated'),
        ('upload', 'File Uploaded'),
        ('download', 'File Downloaded'),
        ('share', 'Shared'),
        ('export', 'Exported'),
        ('print', 'Printed'),
    ]
    
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='action_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} {self.get_action_display()} {self.memo.subject}"


class StatusHistory(models.Model):
    """Track all status changes"""
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='status_history')
    from_status = models.ForeignKey(MemoStatus, on_delete=models.CASCADE, related_name='status_from', null=True, blank=True)
    to_status = models.ForeignKey(MemoStatus, on_delete=models.CASCADE, related_name='status_to')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = "Status Histories"
    
    def __str__(self):
        return f"{self.memo.subject}: {self.from_status} → {self.to_status}"


class CommentThread(models.Model):
    """Comment threads for memo discussions"""
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='comment_threads')
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    is_internal = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.memo.subject} - {self.title}"


class ThreadComment(models.Model):
    """Individual comments in threads"""
    thread = models.ForeignKey(CommentThread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"


# Integration models
class MemoTask(models.Model):
    """Links memos to tasks"""
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='related_tasks')
    task_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    task_object_id = models.PositiveIntegerField()
    task = GenericForeignKey('task_content_type', 'task_object_id')
    relationship_type = models.CharField(max_length=50, choices=[
        ('created_from', 'Created From Memo'),
        ('related_to', 'Related To Memo'),
        ('action_item', 'Action Item From Memo'),
    ])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['memo', 'task_content_type', 'task_object_id']
    
    def __str__(self):
        return f"{self.memo.subject} → Task {self.task_object_id}"


class MemoMeeting(models.Model):
    """Links memos to meetings"""
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='related_meetings')
    meeting_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    meeting_object_id = models.PositiveIntegerField()
    meeting = GenericForeignKey('meeting_content_type', 'meeting_object_id')
    relationship_type = models.CharField(max_length=50, choices=[
        ('scheduled_from', 'Scheduled From Memo'),
        ('discussed_in', 'Discussed In Meeting'),
        ('follow_up', 'Follow-up Meeting'),
    ])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['memo', 'meeting_content_type', 'meeting_object_id']
    
    def __str__(self):
        return f"{self.memo.subject} → Meeting {self.meeting_object_id}"


class RelatedMemo(models.Model):
    """Links memos to other memos"""
    RELATIONSHIP_TYPES = [
        ('response_to', 'Response To'),
        ('follow_up', 'Follow Up'),
        ('reference', 'Reference'),
        ('supersedes', 'Supersedes'),
        ('related', 'Related'),
    ]
    
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='memo_relationships')
    related_memo = models.ForeignKey('Memo', on_delete=models.CASCADE, related_name='related_to_memos')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['memo', 'related_memo', 'relationship_type']
    
    def __str__(self):
        return f"{self.memo.subject} {self.get_relationship_type_display()} {self.related_memo.subject}"
