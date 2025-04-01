from django import forms
from .models import Document, DocumentCategory

class DocumentForm(forms.ModelForm):
    """
    Form for uploading new documents.
    Fields like uploaded_by, content_type, object_id, source_module,
    file_type, file_size are handled in the view.
    """
    # Make category optional or provide a default way to select it
    category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False, # Make optional for now, adjust as needed
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Document
        fields = [
            'title',
            'description',
            'file', # The actual file upload field
            'category',
            'tags',
            'is_confidential',
            # Exclude fields set automatically in the view:
            # 'file_type', 'file_size', 'storage_type', 'drive_file_id',
            # 'drive_view_link', 'status', 'password_protected', 'access_code',
            # 'content_type', 'object_id', 'source_object', 'source_module',
            # 'version', 'parent_document', 'uploaded_by', 'last_accessed', 'expiry_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}),
            'is_confidential': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }