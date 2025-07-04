from django import forms
from .models import (
    Memo, MemoType, MemoCategory, PriorityLevel, MemoStatus, 
    ActionItem, CommentThread, ThreadComment
)
from apps.document_management.models import Document
from apps.organization.models import Department
from django.contrib.auth import get_user_model

User = get_user_model()


class MemoForm(forms.ModelForm):
    """Enhanced memo form for the new memo system"""
    
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
            self.fields['recipient_users'].queryset = User.objects.filter(
                department=user.department
            )
            
            # Show all departments for inter-department memos
            self.fields['recipient_departments'].queryset = Department.objects.filter(
                is_active=True
            ).exclude(id=user.department.id if user.department else None)
        self.fields['sender_external_organization'].widget = forms.TextInput(attrs={'placeholder': 'External Sender Organization'})
        self.fields['recipient_external_name'].widget = forms.TextInput(attrs={'placeholder': 'External Recipient Name'})
        self.fields['recipient_external_organization'].widget = forms.TextInput(attrs={'placeholder': 'External Recipient Organization'})

    def clean(self):
        cleaned_data = super().clean()
        memo_type = cleaned_data.get('memo_type')
        sender_user = cleaned_data.get('sender_user')
        sender_external_name = cleaned_data.get('sender_external_name')
        sender_external_organization = cleaned_data.get('sender_external_organization')
        recipient_departments = cleaned_data.get('recipient_departments')
        recipient_users = cleaned_data.get('recipient_users')
        recipient_external_name = cleaned_data.get('recipient_external_name')
        recipient_external_organization = cleaned_data.get('recipient_external_organization')

        if memo_type == 'internal':
            if not sender_user:
                self.add_error('sender_user', 'Internal memos must have an internal sender.')
            if sender_external_name or sender_external_organization:
                self.add_error('sender_external_name', 'External sender fields should be empty for internal memos.')
            if not (recipient_departments or recipient_users):
                self.add_error('recipient_departments', 'Internal memos must have at least one internal recipient (department or user).')
            if recipient_external_name or recipient_external_organization:
                self.add_error('recipient_external_name', 'External recipient fields should be empty for internal memos.')

        elif memo_type == 'external':
            if not (sender_external_name or sender_external_organization):
                self.add_error('sender_external_name', 'External memos must have an external sender name or organization.')
            if sender_user:
                self.add_error('sender_user', 'Internal sender should be empty for external memos.')
            if not (recipient_external_name or recipient_external_organization):
                self.add_error('recipient_external_name', 'External memos must have an external recipient name or organization.')
            if recipient_departments or recipient_users:
                self.add_error('recipient_departments', 'Internal recipient fields should be empty for external memos.')

        return cleaned_data


class MemoTemplateForm(forms.ModelForm):
    class Meta:
        model = MemoTemplate
        fields = ['name', 'content', 'department'] # added department
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'rich-text-editor'}),
        }

class MemoCommentForm(forms.ModelForm):
    class Meta:
        model = MemoComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter your comment'
            }),
        }