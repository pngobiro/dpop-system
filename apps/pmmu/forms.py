# apps/pmmu/forms.py
from django import forms
from apps.pmmu.models import IndicatorNote # Correct import path to models in pmmu


class IndicatorNoteForm(forms.ModelForm):
    class Meta:
        model = IndicatorNote
        fields = ['note_text']
        widgets = {
            'note_text': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter your note here...'
            })
        }