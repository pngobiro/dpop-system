"""
Enhanced Memo Models for Physical and Digital Memo Tracking

This module contains the new models for the enhanced memo system that supports:
- Physical and digital memo tracking
- Workflow management (office assistant → director → delegation)
- Attachments via Google Drive integration
- Timeline tracking
- Integration with tasks and meetings
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.text import slugify
import uuid
from apps.organization.models import Department


class MemoType(models.Model):
    """Types of memos (Internal, External, Circular, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=10, unique=True, help_text="Short code for reference numbers")
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=True)
    default_workflow = models.ForeignKey(
        'MemoWorkflow', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='default_for_types'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class MemoCategory(models.Model):
    """Categories for organizing memos"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    icon = models.CharField(max_length=50, default='fas fa-file-alt', help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Memo Categories"
        
    def __str__(self):
        return self.name


class PriorityLevel(models.Model):
    """Priority levels for memos"""
    name = models.CharField(max_length=50, unique=True)
    level = models.PositiveIntegerField(unique=True, help_text="1=Highest, 5=Lowest")
    color = models.CharField(max_length=7, help_text="Hex color code")
    description = models.TextField(blank=True)
    response_time_days = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Expected response time in days"
    )
    
    class Meta:
        ordering = ['level']
        
    def __str__(self):
        return f"{self.name} (Level {self.level})"


class MemoStatus(models.Model):
    """Status options for memos"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, help_text="Hex color code")
    is_final = models.BooleanField(default=False, help_text="Cannot change status after reaching this state")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Memo Statuses"
        
    def __str__(self):
        return self.name


class MemoWorkflow(models.Model):
    """Workflow definitions for memo processing"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        help_text="Department this workflow applies to"
    )
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['department', 'name']
        unique_together = ['department', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.department})"


class WorkflowStep(models.Model):
    """Individual steps in a memo workflow"""
    workflow = models.ForeignKey(MemoWorkflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    step_order = models.PositiveIntegerField()
    role_required = models.CharField(
        max_length=100,
        help_text="Required role/permission for this step"
    )
    is_optional = models.BooleanField(default=False)
    time_limit_days = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Time limit for this step in days"
    )
    
    class Meta:
        ordering = ['workflow', 'step_order']
        unique_together = ['workflow', 'step_order']
        
    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order}: {self.name}"


class Memo(models.Model):
    """Enhanced memo model supporting physical and digital tracking"""
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_number = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=500)
    subject = models.TextField(help_text="Brief subject/summary")
    content = models.TextField(blank=True, help_text="Main memo content")
    
    # Classification
    memo_type = models.ForeignKey(MemoType, on_delete=models.PROTECT)
    category = models.ForeignKey(MemoCategory, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.ForeignKey(PriorityLevel, on_delete=models.PROTECT)
    status = models.ForeignKey(MemoStatus, on_delete=models.PROTECT)
    
    # Physical vs Digital
    is_physical = models.BooleanField(default=False, help_text="Is this a physical memo?")
    is_confidential = models.BooleanField(default=False)
    
    # Tracking Information
    received_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Date memo was received (for incoming memos)"
    )
    dispatch_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Date memo was dispatched (for outgoing memos)"
    )
    due_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Date by which action/response is required"
    )
    
    # Sender Information
    sender_internal = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_memos',
        help_text="Internal user who sent the memo"
    )
    sender_external_name = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Name of external sender"
    )
    sender_external_organization = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Organization of external sender"
    )
    sender_external_address = models.TextField(
        blank=True,
        help_text="Address of external sender"
    )
    
    # Recipient Information
    recipient_departments = models.ManyToManyField(
        Department,
        related_name='received_memos',
        blank=True
    )
    recipient_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='received_memos',
        blank=True
    )
    recipient_external_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of external recipient"
    )
    recipient_external_organization = models.CharField(
        max_length=255,
        blank=True,
        help_text="Organization of external recipient"
    )
    recipient_external_address = models.TextField(
        blank=True,
        help_text="Address of external recipient"
    )
    
    # Department and Workflow
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        help_text="Department handling this memo"
    )
    workflow = models.ForeignKey(
        MemoWorkflow,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Workflow being followed"
    )
    current_step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Current step in workflow"
    )
    
    # Filing and Organization
    file_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Physical file reference number"
    )
    tags = models.CharField(
        max_length=1000,
        blank=True,
        help_text="Comma-separated tags for searching"
    )
    
    # System Information
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_memos'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Version Control
    version = models.PositiveIntegerField(default=1)
    is_latest_version = models.BooleanField(default=True)
    original_memo = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='versions',
        help_text="Reference to original memo if this is a version"
    )
    
    # Generic relations for linking to tasks, meetings, etc.
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference_number']),
            models.Index(fields=['status', 'department']),
            models.Index(fields=['received_date']),
            models.Index(fields=['dispatch_date']),
            models.Index(fields=['due_date']),
            models.Index(fields=['is_physical', 'department']),
        ]
        permissions = [
            ("can_approve_memos", "Can approve memos"),
            ("can_dispatch_memos", "Can dispatch memos"),
            ("can_view_confidential_memos", "Can view confidential memos"),
            ("can_manage_workflow", "Can manage memo workflow"),
        ]
    
    def __str__(self):
        return f"{self.reference_number}: {self.title}"
    
    def get_absolute_url(self):
        return reverse('memos:detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        super().save(*args, **kwargs)
    
    def generate_reference_number(self):
        """Generate unique reference number"""
        if not self.department:
            raise ValueError("Cannot generate reference number: Memo has no department")
        
        # Create a department code from the department name (first 3 letters, uppercase)
        dept_code = ''.join([word[0] for word in self.department.name.split()[:3]]).upper()
        if len(dept_code) < 2:
            dept_code = self.department.name[:3].upper()
        
        prefix = f"{self.memo_type.code}/{dept_code}"
        year = timezone.now().year
        
        # Find the last memo with this prefix for this year
        last_memo = Memo.objects.filter(
            reference_number__startswith=f"{prefix}/{year}/"
        ).order_by('-reference_number').first()
        
        if last_memo:
            try:
                last_number = int(last_memo.reference_number.split('/')[-1])
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        return f"{prefix}/{year}/{next_number:04d}"
    
    @property
    def is_overdue(self):
        """Check if memo is overdue"""
        if self.due_date and timezone.now().date() > self.due_date:
            return True
        return False
    
    @property
    def days_until_due(self):
        """Calculate days until due date"""
        if self.due_date:
            delta = self.due_date - timezone.now().date()
            return delta.days
        return None


class ActionItem(models.Model):
    """Action items derived from memos"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='action_items')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_memo_actions'
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='delegated_memo_actions'
    )
    due_date = models.DateField(null=True, blank=True)
    priority = models.ForeignKey(PriorityLevel, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.memo.reference_number}: {self.title}"


class Delegation(models.Model):
    """Track delegation of memo handling"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='delegations')
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='delegated_from'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='delegated_to'
    )
    reason = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    delegated_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='pending')
    
    class Meta:
        ordering = ['-delegated_at']
    
    def __str__(self):
        return f"{self.memo.reference_number}: {self.from_user} → {self.to_user}"


class MemoDocument(models.Model):
    """Link memos to documents (Google Drive integration)"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='documents')
    document = models.ForeignKey(
        'document_management.Document',
        on_delete=models.CASCADE
    )
    document_type = models.CharField(max_length=50, choices=[
        ('original', 'Original Document'),
        ('attachment', 'Attachment'),
        ('signature', 'Signature/Stamp'),
        ('response', 'Response Document'),
        ('version', 'Version'),
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.memo.reference_number}: {self.document.title}"


class MemoTimeline(models.Model):
    """Timeline/history of memo events"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='timeline')
    event_type = models.CharField(max_length=50, choices=[
        ('created', 'Created'),
        ('received', 'Received'),
        ('assigned', 'Assigned'),
        ('forwarded', 'Forwarded'),
        ('delegated', 'Delegated'),
        ('status_changed', 'Status Changed'),
        ('document_added', 'Document Added'),
        ('comment_added', 'Comment Added'),
        ('workflow_step', 'Workflow Step'),
        ('dispatched', 'Dispatched'),
        ('completed', 'Completed'),
    ])
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.memo.reference_number}: {self.event_type} at {self.timestamp}"


class ActionLog(models.Model):
    """Detailed action log for audit purposes"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='action_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.memo.reference_number}: {self.action} by {self.user}"


class StatusHistory(models.Model):
    """Track status changes"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.ForeignKey(
        MemoStatus,
        on_delete=models.PROTECT,
        related_name='status_changes_from',
        null=True,
        blank=True
    )
    to_status = models.ForeignKey(
        MemoStatus,
        on_delete=models.PROTECT,
        related_name='status_changes_to'
    )
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
    
    def __str__(self):
        from_status = self.from_status.name if self.from_status else 'None'
        return f"{self.memo.reference_number}: {from_status} → {self.to_status.name}"


class CommentThread(models.Model):
    """Comment threads on memos"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='comment_threads')
    title = models.CharField(max_length=255, blank=True)
    is_internal = models.BooleanField(
        default=True,
        help_text="Internal comments visible only to department staff"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.memo.reference_number}: {self.title or 'Thread'}"


class ThreadComment(models.Model):
    """Individual comments in a thread"""
    thread = models.ForeignKey(CommentThread, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"


# Integration Models

class MemoTask(models.Model):
    """Link memos to tasks"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='related_tasks')
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='related_memos')
    relationship_type = models.CharField(max_length=50, choices=[
        ('derived_from', 'Task Derived From Memo'),
        ('referenced_in', 'Task Referenced in Memo'),
        ('response_to', 'Task is Response to Memo'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['memo', 'task']
    
    def __str__(self):
        return f"{self.memo.reference_number} ↔ {self.task.title}"


class MemoMeeting(models.Model):
    """Link memos to meetings"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='related_meetings')
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, related_name='related_memos')
    relationship_type = models.CharField(max_length=50, choices=[
        ('agenda_item', 'Memo as Agenda Item'),
        ('follow_up', 'Meeting Follow-up to Memo'),
        ('referenced_in', 'Memo Referenced in Meeting'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['memo', 'meeting']
    
    def __str__(self):
        return f"{self.memo.reference_number} ↔ {self.meeting.title}"


class RelatedMemo(models.Model):
    """Link related memos"""
    from_memo = models.ForeignKey(
        Memo,
        on_delete=models.CASCADE,
        related_name='related_memos_from'
    )
    to_memo = models.ForeignKey(
        Memo,
        on_delete=models.CASCADE,
        related_name='related_memos_to'
    )
    relationship_type = models.CharField(max_length=50, choices=[
        ('response_to', 'Response To'),
        ('follow_up', 'Follow Up'),
        ('reference', 'References'),
        ('supersedes', 'Supersedes'),
        ('related', 'Related'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['from_memo', 'to_memo']
    
    def __str__(self):
        return f"{self.from_memo.reference_number} → {self.to_memo.reference_number}"
