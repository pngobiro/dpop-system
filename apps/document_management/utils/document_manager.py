# apps/document_management/utils/document_manager.py
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from ..models import Document, DocumentActivity, DocumentAccess
import os
import mimetypes

class DocumentManager:
    @staticmethod
    def attach_document(file, source_object, uploaded_by, **kwargs):
        """
        Attach a document to any model instance
        
        Args:
            file: The file to upload (UploadedFile instance)
            source_object: The model instance this document belongs to
            uploaded_by: User instance who is uploading the document
            **kwargs: Additional document attributes
        
        Returns:
            Document instance
        """
        # Get content type for the source object
        content_type = ContentType.objects.get_for_model(source_object)
        
        # Determine file type and size
        file_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
        file_extension = os.path.splitext(file.name)[1].lower()
        
        # Create document instance
        document = Document(
            title=kwargs.get('title', file.name),
            description=kwargs.get('description', ''),
            file=file,
            file_type=file_type,
            file_size=file.size,
            content_type=content_type,
            object_id=source_object.id,
            source_module=source_object._meta.app_label,
            uploaded_by=uploaded_by,
            category_id=kwargs.get('category_id'),
            is_confidential=kwargs.get('is_confidential', False),
            status=kwargs.get('status', 'draft'),
            storage_type=kwargs.get('storage_type', 'local'),
            version=kwargs.get('version', '1.0')
        )
        document.save()
        
        # Record the activity
        DocumentActivity.objects.create(
            document=document,
            user=uploaded_by,
            action='upload',
            action_details=f"Document uploaded from {source_object._meta.model_name}"
        )
        
        # Set up initial access
        DocumentAccess.objects.create(
            document=document,
            user=uploaded_by,
            permission_type='admin',
            granted_by=uploaded_by
        )
        
        return document

    @staticmethod
    def get_module_documents(source_object):
        """Get all documents attached to a specific model instance"""
        content_type = ContentType.objects.get_for_model(source_object)
        return Document.objects.filter(
            content_type=content_type,
            object_id=source_object.id
        )

    @staticmethod
    def get_user_accessible_documents(user, module_name=None):
        """Get all documents a user has access to, optionally filtered by module"""
        accessible_docs = Document.objects.filter(
            documentaccess__user=user,
            documentaccess__is_active=True
        )
        
        if module_name:
            accessible_docs = accessible_docs.filter(source_module=module_name)
            
        return accessible_docs

    @staticmethod
    def record_document_access(document, user, action, **kwargs):
        """Record document activity"""
        DocumentActivity.objects.create(
            document=document,
            user=user,
            action=action,
            action_details=kwargs.get('details', ''),
            ip_address=kwargs.get('ip_address'),
            user_agent=kwargs.get('user_agent')
        )
        
        # Update last accessed timestamp
        document.last_accessed = timezone.now()
        document.save(update_fields=['last_accessed'])

    @staticmethod
    def grant_access(document, user, granted_by, permission_type='view', expires_at=None):
        """Grant document access to a user"""
        access, created = DocumentAccess.objects.get_or_create(
            document=document,
            user=user,
            defaults={
                'permission_type': permission_type,
                'granted_by': granted_by,
                'expires_at': expires_at,
                'is_active': True
            }
        )
        
        if not created:
            access.permission_type = permission_type
            access.expires_at = expires_at
            access.is_active = True
            access.save()
            
        DocumentActivity.objects.create(
            document=document,
            user=granted_by,
            action='share',
            action_details=f"Access granted to {user.email} with {permission_type} permissions"
        )
        
        return access

    @staticmethod
    def revoke_access(document, user, revoked_by):
        """Revoke user's access to a document"""
        try:
            access = DocumentAccess.objects.get(document=document, user=user)
            access.is_active = False
            access.save()
            
            DocumentActivity.objects.create(
                document=document,
                user=revoked_by,
                action='share',
                action_details=f"Access revoked for {user.email}"
            )
            
            return True
        except DocumentAccess.DoesNotExist:
            return False