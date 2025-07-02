
from django.db import models
from django.conf import settings
from apps.organization.models import Department
from apps.document_management.models import Document, DocumentCategory
from django.contrib.contenttypes.fields import GenericForeignKey, ContentType # Import GenericForeignKey and ContentType

class MemoTemplate(models.Model):
    """Templates for different types of memos"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    memo_type = models.CharField(max_length=50, choices=[
        ('internal', 'Internal Memo'),
        ('external', 'External Letter'),
        ('circular', 'Circular')
    ])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.get_memo_type_display()}"

class Memo(models.Model):
    """Main memo model"""
    MEMO_STATUS = [
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('needs_clarification', 'Needs Clarification'),
        ('completed', 'Completed'),
    ]
    
    MEMO_TYPE = [
        ('internal', 'Internal Memo'),
        ('external', 'External Letter'),
        ('circular', 'Circular')
    ]

    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=100, unique=True)
    memo_type = models.CharField(max_length=50, choices=MEMO_TYPE)
    template = models.ForeignKey(MemoTemplate, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=MEMO_STATUS, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Sender Information
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_memos', help_text="Internal user who sent the memo.")
    sender_external_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of external sender, if applicable.")
    sender_external_organization = models.CharField(max_length=255, blank=True, null=True, help_text="Organization of external sender, if applicable.")

    # Recipient Information (Internal and External)
    recipient_external_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of external recipient, if applicable.")
    recipient_external_organization = models.CharField(max_length=255, blank=True, null=True, help_text="Organization of external recipient, if applicable.")

    # Due Date for action/response
    due_date = models.DateField(null=True, blank=True, help_text="Date by which action or response is required.")
    
    # Main document - stores the final version
    document = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='memo_main_document'
    )
    
    # Generic Relation to a source object (e.g., Task, Meeting)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL, # Or models.CASCADE, depending on desired behavior
        null=True,
        blank=True,
        help_text="The content type of the object this memo is related to (e.g., Task, Meeting)."
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="The ID of the related object."
    )
    # This is the GenericForeignKey itself, providing easy access to the related object
    source_object = GenericForeignKey('content_type', 'object_id')

    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    version_number = models.PositiveIntegerField(default=1)
    
    # Recipients and visibility
    recipient_departments = models.ManyToManyField(
        Department, related_name='received_memos', blank=True
    )
    recipient_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='receipent_memos', blank=True
    )
    is_confidential = models.BooleanField(default=False)
    
    # For external memos
    external_recipient = models.CharField(max_length=255, blank=True, null=True)
    external_organization = models.CharField(max_length=255, blank=True, null=True)
    
    # Classification and filing
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    file_number = models.CharField(max_length=100, blank=True)  # For physical filing reference
    
    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_approve_memos", "Can approve memos"),
            ("can_publish_memos", "Can publish memos"),
            ("view_department_memos", "Can view department memos"),
        ]

    def create_document(self, file_obj, title_suffix=""):
        """Helper method to create a Document for this memo"""
        from apps.document_management.utils import DocumentManager

        title = f"{self.title}{title_suffix}"
        return DocumentManager.attach_document(
            file=file_obj,
            source_object=self,
            uploaded_by=self.created_by,
            title=title,
            description=f"Document for memo: {self.reference_number}",
            category=DocumentCategory.objects.get_or_create(
                name="Memos",
                defaults={'description': 'Documents related to memos'}
            )[0],
            is_confidential=self.is_confidential,
            status='draft' if self.status == 'draft' else 'approved'
        )

class MemoVersion(models.Model):
    """Track different versions of a memo"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    content = models.TextField()
    document = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memo_versions'
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['memo', 'version_number']
        ordering = ['-version_number']

class MemoApproval(models.Model):
    """Track approval workflow for memos"""
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('skipped', 'Skipped')
    ]
    
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    level = models.PositiveIntegerField(help_text="Approval hierarchy level")
    
    # Document containing approval signature or stamp
    signature_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memo_approvals'
    )
    
    class Meta:
        ordering = ['level']
        unique_together = ['memo', 'approver', 'level']

class MemoComment(models.Model):
    """Comments and feedback on memos"""
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, 
                              related_name='replies')
    is_internal = models.BooleanField(default=True, 
                                    help_text="Internal comments are only visible to memo creators and approvers")
    
    # Attachments to comments (like screenshots or supporting documents)
    attachments = models.ManyToManyField(Document, blank=True, related_name='memo_comments')

class MemoActivity(models.Model):
    """Audit trail of all memo-related activities"""
    ACTION_TYPES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('status_change', 'Status Changed'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('comment', 'Commented'),
        ('view', 'Viewed'),
        ('download', 'Downloaded'),
        ('share', 'Shared')
    ]
    
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_details = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    # Related document if action involves a document
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memo_activities'
    )