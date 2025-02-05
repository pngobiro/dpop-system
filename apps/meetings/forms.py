# apps/meetings/forms.py
from django import forms
from .models import Meeting, MeetingParticipant, MeetingDocument, MeetingAction

class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['start_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['end_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['participants'].widget.attrs['class'] = 'form-control select2'
        
        # Make virtual meeting fields not required initially
        self.fields['virtual_meeting_url'].required = False
        self.fields['virtual_meeting_id'].required = False
        self.fields['virtual_meeting_password'].required = False
        self.fields['physical_location'].required = False

    def clean(self):
        cleaned_data = super().clean()
        meeting_mode = cleaned_data.get('meeting_mode')

        # Validate based on meeting mode
        if meeting_mode == 'virtual' or meeting_mode == 'hybrid':
            if not cleaned_data.get('virtual_meeting_url'):
                self.add_error('virtual_meeting_url', 'Virtual meeting URL is required for virtual/hybrid meetings')

        if meeting_mode == 'physical' or meeting_mode == 'hybrid':
            if not cleaned_data.get('physical_location'):
                self.add_error('physical_location', 'Physical location is required for physical/hybrid meetings')

        return cleaned_data

    class Meta:
        model = Meeting
        fields = [
            'title', 'department', 'meeting_type', 'meeting_mode',
            'date', 'start_time', 'end_time',
            'physical_location', 'virtual_platform',
            'virtual_meeting_url', 'virtual_meeting_id',
            'virtual_meeting_password', 'agenda', 'participants'
        ]
        widgets = {
            'agenda': forms.Textarea(attrs={'rows': 4}),
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
        
        

# apps/meetings/forms.py

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