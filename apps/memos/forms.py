from django import forms
from .models import Memo, MemoTemplate, MemoComment
from apps.document_management.models import Document

class MemoForm(forms.ModelForm):
    document = forms.FileField(required=False)
    template = forms.ModelChoiceField(
        queryset=MemoTemplate.objects.none(),
        required=False,
        empty_label="Select a template"
    )

    class Meta:
        model = Memo
        fields = [
            'title', 'memo_type', 'content', 'recipient_departments',
            'recipient_users', 'is_confidential', 'external_recipient',
            'external_organization', 'tags', 'file_number'
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
        
        if user:
            # Filter templates based on user's department
            self.fields['template'].queryset = MemoTemplate.objects.filter(
                models.Q(department=user.department) | 
                models.Q(department__isnull=True)
            )

    def clean(self):
        cleaned_data = super().clean()
        memo_type = cleaned_data.get('memo_type')
        external_recipient = cleaned_data.get('external_recipient')

class MemoTemplateForm(forms.ModelForm):
    class Meta:
        model = MemoTemplate
        fields = ['name', 'content', 'department']
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