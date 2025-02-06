# apps/document_management/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Document Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Document(models.Model):
    STORAGE_CHOICES = [
        ('local', 'Local Storage'),
        ('google_drive', 'Google Drive')
    ]
    
    DOCUMENT_STATUS = [
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived')
    ]

    # Basic fields
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    file_type = models.CharField(max_length=50)  # e.g., pdf, doc, image
    file_size = models.BigIntegerField()  # in bytes
    
    # Classification
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True)
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    
    # Storage information
    storage_type = models.CharField(max_length=20, choices=STORAGE_CHOICES, default='local')
    drive_file_id = models.CharField(max_length=100, blank=True, null=True)
    drive_view_link = models.URLField(blank=True, null=True)
    
    # Security and access
    is_confidential = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=DOCUMENT_STATUS, default='draft')
    password_protected = models.BooleanField(default=False)
    access_code = models.CharField(max_length=100, blank=True, null=True)
    
    # Source tracking (Generic relation to any model)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    source_object = GenericForeignKey('content_type', 'object_id')
    source_module = models.CharField(max_length=50, help_text="Name of the module this document belongs to")
    
    # Version control
    version = models.CharField(max_length=50, default='1.0')
    parent_document = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='versions')
    
    # Metadata
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (v{self.version})"

    def get_file_url(self):
        if self.storage_type == 'google_drive' and self.drive_view_link:
            return self.drive_view_link
        return self.file.url if self.file else None

class DocumentAccess(models.Model):
    """Track document access permissions and history"""
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('edit', 'Edit'),
        ('admin', 'Full Admin')
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_CHOICES)
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='granted_permissions')
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['document', 'user']

class DocumentActivity(models.Model):
    """Track all document-related activities"""
    ACTION_CHOICES = [
        ('upload', 'Upload'),
        ('view', 'View'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('share', 'Share'),
        ('download', 'Download'),
        ('print', 'Print'),
        ('status_change', 'Status Change')
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Document Activities"
        ordering = ['-timestamp']