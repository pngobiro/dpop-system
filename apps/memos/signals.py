# apps/memos/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Memo, MemoActivity, MemoApproval
from django.utils import timezone

@receiver(post_save, sender=Memo)
def create_memo_activity(sender, instance, created, **kwargs):
    if created:
        MemoActivity.objects.create(
            memo=instance,
            user=instance.created_by,
            action='create',
            action_details={'status': instance.status}
        )

@receiver(pre_save, sender=Memo)
def track_memo_changes(sender, instance, **kwargs):
    if instance.pk:  # Only for existing instances
        old_instance = Memo.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            MemoActivity.objects.create(
                memo=instance,
                user=instance.created_by,
                action='status_change',
                action_details={
                    'old_status': old_instance.status,
                    'new_status': instance.status
                }
            )