from django import forms
from .models import (
    Memo, MemoType, MemoCategory, PriorityLevel, MemoStatus, 
    ActionItem, CommentThread, ThreadComment
)
from apps.document_management.models import Document
from apps.organization.models import Department
from django.contrib.auth import get_user_model

User = get_user_model()


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MemoForm(forms.ModelForm):
    """Enhanced memo form for the new memo system"""
    
    # Add file attachments field (not part of the model, handled separately)
    attachments = MultipleFileField(
        required=False,
        help_text='Upload multiple files (PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, JPG, PNG). Max 10MB per file.'
    )
    
    class Meta:
        model = Memo
        fields = [
            'title', 'subject', 'content', 'memo_type', 'category', 'priority', 
            'is_physical', 'is_confidential', 'due_date',
            'sender_internal', 'sender_external_name', 'sender_external_organization', 'sender_external_address',
            'recipient_departments', 'recipient_users', 
            'recipient_external_name', 'recipient_external_organization', 'recipient_external_address',
            'file_number', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter memo title'}),
            'subject': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief subject/summary'}),
            'content': forms.Textarea(attrs={'class': 'form-control rich-text-editor', 'rows': 10}),
            'memo_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'is_physical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_confidential': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sender_internal': forms.Select(attrs={'class': 'form-select select2'}),
            'sender_external_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'External sender name'}),
            'sender_external_organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'External sender organization'}),
            'sender_external_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'External sender address'}),
            'recipient_departments': forms.SelectMultiple(attrs={'class': 'form-select select2', 'data-placeholder': 'Select departments'}),
            'recipient_users': forms.SelectMultiple(attrs={'class': 'form-select select2', 'data-placeholder': 'Select users'}),
            'recipient_external_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'External recipient name'}),
            'recipient_external_organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'External recipient organization'}),
            'recipient_external_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'External recipient address'}),
            'file_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Physical file reference'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'data-role': 'tagsinput', 'placeholder': 'Enter tags separated by commas'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)

        # Set user's department if provided
        if department:
            self.instance.department = department

        # Set initial sender if creating new memo
        if not self.instance.pk and user:
            self.initial['sender_internal'] = user

        # Filter querysets based on user's department
        if user and user.department:
            # Only show users from same department for internal recipients
            # Since users can belong to multiple departments, we need to filter through the user_roles
            self.fields['recipient_users'].queryset = User.objects.filter(
                user_roles__role__department=user.department,
                user_roles__is_active=True
            ).distinct()
            
            # Show all departments for inter-department memos
            self.fields['recipient_departments'].queryset = Department.objects.filter(
                is_active=True
            ).exclude(id=user.department.id if user.department else None)

    def clean(self):
        cleaned_data = super().clean()
        sender_internal = cleaned_data.get('sender_internal')
        sender_external_name = cleaned_data.get('sender_external_name')
        recipient_departments = cleaned_data.get('recipient_departments')
        recipient_users = cleaned_data.get('recipient_users')
        recipient_external_name = cleaned_data.get('recipient_external_name')

        # Validate sender information
        if not sender_internal and not sender_external_name:
            raise forms.ValidationError("Either internal sender or external sender name must be provided.")

        # Validate recipient information
        has_internal_recipients = recipient_departments or recipient_users
        has_external_recipients = recipient_external_name or cleaned_data.get('recipient_external_organization')
        
        if not has_internal_recipients and not has_external_recipients:
            raise forms.ValidationError("At least one recipient must be specified.")

        return cleaned_data


class ActionItemForm(forms.ModelForm):
    """Form for creating action items from memos"""
    
    class Meta:
        model = ActionItem
        fields = ['title', 'description', 'assigned_to', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Action item title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select select2'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }


class CommentThreadForm(forms.ModelForm):
    """Form for creating comment threads"""
    
    class Meta:
        model = CommentThread
        fields = ['title', 'is_internal']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thread title (optional)'}),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ThreadCommentForm(forms.ModelForm):
    """Form for adding comments to threads"""
    
    class Meta:
        model = ThreadComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your comment...'
            }),
        }
