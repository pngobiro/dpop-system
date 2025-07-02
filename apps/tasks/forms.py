from django import forms
from .models import Task, Comment, Project
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from apps.meetings.models import Meeting # Import Meeting model

User = get_user_model()

class ProjectForm(forms.ModelForm):
    """
    Form for creating new projects.
    Department and Owner will be set in the view.
    """
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter a brief project description'}),
        }
        help_texts = {
            'name': 'A clear and concise name for the project.',
            'description': 'Optional description of the project goals and scope.',
        }


class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks.
    Allows setting due date by specific date OR number of days from today.
    """
    assignees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Assign To",
        help_text="Select one or more users to assign this task to."
    )

    # Allow setting due date relative to today
    due_in_days = forms.IntegerField(
        required=False,
        min_value=0,
        label="Or Due In (Days from Today)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 7'}),
        help_text="Set a due date relative to today. Overrides specific date if both are entered."
    )

    due_date = forms.DateField(
        required=False,
        label="Due Date (Specific)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Optional: Select a specific deadline."
    )
    start_date = forms.DateField( # Add start_date field
        required=False,
        label="Start Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Optional: Select a start date for the task."
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        # Make project field read-only in the form
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'})
    )

    # New field for generic relation to Meeting
    related_meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(),
        required=False,
        label="Related Meeting",
        help_text="Link this task to an existing meeting."
    )

    class Meta:
        model = Task
        fields = [
            'project',
            'title',
            'description',
            'status',
            'priority',
            'assignees',
            'start_date',
            'due_date',
            'due_in_days',
            'related_meeting', # Add new field to Meta
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'project': 'The project this task belongs to (read-only).',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If this is an existing task, populate assignees field
        if self.instance.pk:
            self.fields['assignees'].initial = self.instance.assignees.all()
            # If task is linked to a meeting, set initial value for related_meeting
            if self.instance.source_object and isinstance(self.instance.source_object, Meeting):
                self.fields['related_meeting'].initial = self.instance.source_object

    def clean(self):
        """
        Calculate due_date from due_in_days if provided.
        due_in_days takes precedence.
        """
        cleaned_data = super().clean()
        due_in_days = cleaned_data.get('due_in_days')

        if due_in_days is not None: # Check if None, not just falsy (0 is valid)
            try:
                days = int(due_in_days)
                if days >= 0:
                    calculated_date = timezone.now().date() + datetime.timedelta(days=days)
                    # Set the actual due_date field based on calculation
                    cleaned_data['due_date'] = calculated_date
                else:
                    self.add_error('due_in_days', 'Please enter a non-negative number of days.')
            except (ValueError, TypeError):
                 self.add_error('due_in_days', 'Please enter a valid number of days.')

        return cleaned_data


class ReassignTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assignees']
        widgets = {
            'assignees': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'assignees': "Assign To",
        }
        help_texts = {
            'assignees': "Select one or more users to assign this task to.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the queryset for assignees is correct
        self.fields['assignees'].queryset = User.objects.all()


class CommentForm(forms.ModelForm):
    """
    Form for adding comments to tasks.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add your comment...'
            }),
        }
        labels = {
            'content': '', # Hide the label, use placeholder
        }