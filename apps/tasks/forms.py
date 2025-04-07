from django import forms
from .models import Task, Comment, Project
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

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
    # Allow setting due date relative to today
    due_in_days = forms.IntegerField(
        required=False,
        min_value=0,
        label="Or Due In (Days from Today)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 7'}),
        help_text="Set a due date relative to today. Overrides specific date if both are entered."
    )

    # Assignee field removed as per request for this specific form usage
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

    class Meta:
        model = Task
        fields = [
            'project',
            'title',
            'description',
            'status',
            'priority',
            # 'assignee', # Removed from fields list
            'start_date', # Add start_date
            'due_date', # Keep original field
            'due_in_days', # Add new relative field
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'project': 'The project this task belongs to (read-only).',
            # 'assignee': 'Select the user responsible for this task (optional).', # Removed help text
            # Removed help_text for due_date as it's now part of the field definition
        }

    def clean(self):
        """
        Calculate due_date from due_in_days if provided.
        due_in_days takes precedence.
        """
        cleaned_data = super().clean()
        due_in_days = cleaned_data.get('due_in_days')
        due_date = cleaned_data.get('due_date') # Original due_date

        if due_in_days is not None: # Check if None, not just falsy (0 is valid)
            try:
                days = int(due_in_days)
                if days >= 0:
                    calculated_date = timezone.now().date() + datetime.timedelta(days=days)
                    # Set the actual due_date field based on calculation
                    cleaned_data['due_date'] = calculated_date
                    # Optionally clear due_in_days after calculation if desired,
                    # but keeping it might be useful for display logic later.
                    # cleaned_data['due_in_days'] = None
                else:
                    # Should be caught by min_value, but double-check
                    self.add_error('due_in_days', 'Please enter a non-negative number of days.')
            except (ValueError, TypeError):
                 self.add_error('due_in_days', 'Please enter a valid number of days.')
        # No need for explicit check if both are entered, as due_in_days calculation overwrites due_date

        return cleaned_data


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