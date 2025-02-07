
# apps/mail/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PhysicalMail, MailActivity, MailAssignment, generate_tracking_number  # Import models
from django.utils import timezone

@receiver(post_save, sender=PhysicalMail)
def create_mail_activity(sender, instance, created, **kwargs):
    if created:
        MailActivity.objects.create(
            mail=instance,
            user=instance.created_by,
            action='register',
            location=instance.department.name,  # Assuming location is department
            notes=f'Mail registered with tracking number {instance.tracking_number}'
        )

@receiver(pre_save, sender=PhysicalMail)
def set_tracking_number(sender, instance, **kwargs):
     if not instance.tracking_number:
        instance.tracking_number = generate_tracking_number()