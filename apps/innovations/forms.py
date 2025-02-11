# apps/innovations/forms.py
from django import forms
from .models import Innovation, InnovationAttachment
from django.forms import inlineformset_factory


class InnovationForm(forms.ModelForm):
    class Meta:
        model = Innovation
        fields = [
            'court',
            'station',
            'financial_year',
            'title',
            'is_replication',
            'source_court',
            'category',
            'situation_before',
            'description',
            'solution',
            'replication_potential',
            'individuals_involved',
            'stakeholders_affected',
            'status', # status in the form
        ]

        widgets = {
            'situation_before': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'solution': forms.Textarea(attrs={'rows': 5}),
            'replication_potential': forms.Textarea(attrs={'rows': 3}),
            'individuals_involved': forms.Textarea(attrs={'rows': 3}),
            'stakeholders_affected': forms.Textarea(attrs={'rows': 3}),

            'court': forms.Select(attrs={'class': 'form-control'}),
            'station': forms.TextInput(attrs={'class': 'form-control'}),
            'financial_year': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'source_court': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}), # Added category
             'status': forms.Select(attrs={'class': 'form-control'}),# added ststus in the form
        }

        # help text
        help_texts = {
          'is_replication': 'Check this box if this innovation is a replication of an existing innovation.',
          'source_court': 'If this is a replication, specify the original court/tribunal/directorate/registry.',
        }
      
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       # Set up choices for the 'category' field, based on SECTION II of your form.
       self.fields['category'].choices = [
          ('', 'Select Category'),  # Add a blank option at the top
          ('efficiency', 'Initiatives that improve efficiency and effectiveness in service delivery (Court user satisfaction)'),
          ('vulnerable', 'Initiatives that are responsive to vulnerable and marginalised groups'),
          ('security', 'Initiatives that enhance security, safety and convenience'),
          ('access', 'Initiatives that enhance expansion of doorways to Justice'),
          ('partnerships', 'Initiatives in partnerships with other stakeholders in justice chain'),
          ('mentorship', 'Initiatives that enhance mentorship, leadership and governance'),
          ('financial', 'Initiatives that improve financial management and save cost'),
          ('employee', 'Initiatives that improve employee satisfaction and mental wellness'),
          ('environment', 'Initiatives that improve work environment and/or mitigate effects of climate change'),
          ('other', 'Others (specify)'),
        ]
        
    # def clean, to check the required based on a selection

    def clean(self):
      cleaned_data = super().clean()
      is_replication = cleaned_data.get('is_replication')
      source_court = cleaned_data.get('source_court')

      if is_replication and not source_court:
          self.add_error('source_court', 'Source court is required if this is a replication.')

      return cleaned_data

class InnovationAttachmentForm(forms.ModelForm):
    class Meta:
        model = InnovationAttachment
        fields = ['file']

# Create an inline formset for attachments
InnovationAttachmentFormSet = inlineformset_factory(
    Innovation,
    InnovationAttachment,
    form=InnovationAttachmentForm,
    extra=1,  # Number of empty forms to display
    can_delete=True,  # Allow deleting existing attachments
)