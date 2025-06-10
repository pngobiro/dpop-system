# apps/meetings/forms.py
from django import forms
from django.utils import timezone
from .models import Meeting, MeetingParticipant, MeetingDocument, MeetingAction

class MeetingForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make end_time not required
        self.fields['end_time'].required = False

        # Apply form-control class to all fields
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            field.widget.attrs.update({
                'class': css_class,
                'data-required': field.required
            })

        # Special handling for specific fields
        self.fields['date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True,
            'min': timezone.now().date().isoformat()
        })
        self.fields['start_time'].widget = forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'required': True
        })
        self.fields['end_time'].widget = forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'required': False
        })
        
        # Remove department field since it's set automatically
        if 'department' in self.fields:
            del self.fields['department']
        
        # Handle virtual meeting fields
        for field in ['virtual_meeting_id', 'virtual_meeting_password', 'physical_location']:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'data-conditional': 'true'
            })
            
        # Special handling for virtual_meeting_url to be more flexible
        self.fields['virtual_meeting_url'].required = False
        self.fields['virtual_meeting_url'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://meet.google.com/abc-defg-hij or meeting ID',
            'data-conditional': 'true'
        })
        self.fields['virtual_meeting_url'].help_text = 'Required for virtual or hybrid meetings'
        self.fields['physical_location'].help_text = 'Required for physical or hybrid meetings'

    def clean(self):
        cleaned_data = super().clean()
        
        # Basic date/time validation
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if date and start_time:
            if end_time and start_time >= end_time:
                self.add_error('end_time', 'End time must be after start time')
        
        # Meeting mode validation
        meeting_mode = cleaned_data.get('meeting_mode')
        if meeting_mode:
            if meeting_mode in ['virtual', 'hybrid']:
                if not cleaned_data.get('virtual_meeting_url'):
                    self.add_error('virtual_meeting_url', 'Virtual meeting URL is required for virtual/hybrid meetings')
                if not cleaned_data.get('virtual_platform'):
                    self.add_error('virtual_platform', 'Virtual platform must be selected for virtual/hybrid meetings')
            
            if meeting_mode in ['physical', 'hybrid']:
                if not cleaned_data.get('physical_location'):
                    self.add_error('physical_location', 'Physical location is required for physical/hybrid meetings')
        
        return cleaned_data

    class Meta:
        model = Meeting
        fields = [
            'title', 'meeting_type', 'meeting_mode',  # Removed department from fields
            'date', 'start_time', 'end_time',
            'physical_location', 'virtual_platform',
            'virtual_meeting_url', 'virtual_meeting_id',
            'virtual_meeting_password', 'agenda'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_type': forms.Select(attrs={'class': 'form-control'}),
            'meeting_mode': forms.Select(attrs={'class': 'form-control'}),
            'physical_location': forms.TextInput(attrs={'class': 'form-control'}),
            'virtual_platform': forms.Select(attrs={'class': 'form-control'}),
            'virtual_meeting_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://meet.google.com/abc-defg-hij or meeting ID'
            }),
            'virtual_meeting_id': forms.TextInput(attrs={'class': 'form-control'}),
            'virtual_meeting_password': forms.TextInput(attrs={'class': 'form-control'}),
            'agenda': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        
class MeetingActionForm(forms.ModelForm):
    class Meta:
        model = MeetingAction
        fields = ['description', 'assigned_to', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter action item description'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = 'Action Item Description'
        self.fields['assigned_to'].label = 'Assign To'
        self.fields['due_date'].label = 'Due Date'
        

class MeetingDocumentForm(forms.ModelForm):
    DOCUMENT_TYPES = [
        ('agenda', 'Agenda'),
        ('minutes', 'Minutes'),
        ('presentation', 'Presentation'),
        ('report', 'Report'),
        ('other', 'Other')
    ]
    
    document_type = forms.ChoiceField(
        choices=DOCUMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes about this document'
        })
    )

    class Meta:
        model = MeetingDocument
        fields = ['document_type', 'file', 'notes']
        
    def save(self, meeting, commit=True):
        instance = super().save(commit=False)
        instance.meeting = meeting
        
        if commit:
            instance.save()
        return instance