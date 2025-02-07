# apps/mail/forms.py
from django import forms
from .models import PhysicalMail, MailAttachment, MailAssignment, MailMovement

class PhysicalMailForm(forms.ModelForm):
    class Meta:
        model = PhysicalMail
        fields = [
            'mail_type', 'subject', 'description', 'department',
            'priority', 'confidential', 'file_number',
            'delivery_method', 'weight', 'postage_cost',
            'courier_name', 'courier_tracking_number',
            'sender_name', 'sender_address', 'sender_phone',
            'recipient_name', 'recipient_address', 'recipient_phone',
            'requires_response', 'response_deadline'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'sender_address': forms.Textarea(attrs={'rows': 3}),
            'recipient_address': forms.Textarea(attrs={'rows': 3}),
            'response_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class MailAttachmentForm(forms.ModelForm):
    class Meta:
        model = MailAttachment
        fields = ['name', 'description', 'attachment_type', 'quantity', 'condition', 'digital_copy']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MailMovementForm(forms.ModelForm):
    class Meta:
        model = MailMovement
        fields = ['from_location', 'to_location', 'notes', 'received_by']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'received_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MailAssignmentForm(forms.ModelForm):
    class Meta:
        model = MailAssignment
        fields = [
            'assigned_to', 'due_date', 'notes', 
            'current_location', 'acknowledgment_required'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class MailReceiptForm(forms.Form):
    """Form for recording receipt of physical mail"""
    received_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    received_by = forms.CharField(max_length=255)
    condition = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Describe the condition of the mail when received"
    )
    seal_intact = forms.BooleanField(required=False)
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

class MailDispatchForm(forms.Form):
    """Form for recording dispatch of physical mail"""
    dispatch_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    dispatched_by = forms.CharField(max_length=255)
    delivery_method = forms.ChoiceField(choices=PhysicalMail.DELIVERY_METHOD_CHOICES)
    courier_name = forms.CharField(max_length=100, required=False)
    tracking_number = forms.CharField(max_length=100, required=False)
    postage_cost = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )