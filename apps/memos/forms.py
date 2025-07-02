from django import forms
from .models import Memo, MemoTemplate, MemoComment
from apps.document_management.models import Document
from django.db.models import Q # Import Q

class MemoForm(forms.ModelForm):
    document = forms.FileField(required=False)
    template = forms.ModelChoiceField(
        queryset=MemoTemplate.objects.none(),  # Start with an empty queryset
        required=False,
        empty_label="Select a template"
    )

    class Meta:
        model = Memo
        fields = [
            'title', 'memo_type', 'content', 'priority', 'due_date',
            'sender_user', 'sender_external_name', 'sender_external_organization',
            'recipient_departments', 'recipient_users', 'recipient_external_name',
            'recipient_external_organization', 'is_confidential', 'tags', 'file_number'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'rich-text-editor'}),
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            'recipient_departments': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': 'Select departments'}
            ),
            'recipient_users': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': 'Select users'}
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Set initial sender_user if creating a new memo
        if not self.instance.pk and user:
            self.initial['sender_user'] = user

        if user:
            self.fields['template'].queryset = MemoTemplate.objects.filter(
                Q(department=user.department) | Q(department__isnull=True)
            )

        # Update widgets for new fields
        self.fields['priority'].widget = forms.Select(choices=Memo.PRIORITY_CHOICES)
        self.fields['due_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['sender_user'].widget = forms.Select(attrs={'class': 'select2', 'data-placeholder': 'Select internal sender'})
        self.fields['sender_external_name'].widget = forms.TextInput(attrs={'placeholder': 'External Sender Name'})
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