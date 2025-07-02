from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task, TaskHistory

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    """ 
    Handles post-save operations for tasks, including history tracking and notifications.
    """
    # We need to get the state of the object before it was saved
    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        old_instance = None

    # Determine the user who made the change (if available)
    user = getattr(instance, '_user', None)

    # 1. Handle Task Creation
    if created:
        change_description = "Task created."
        TaskHistory.objects.create(
            task=instance,
            user=user,
            change_description=change_description,
            task_state=instance.to_dict() # Assumes a to_dict() method on Task model
        )
        # Notify assignees on creation
        if instance.assignees.exists():
            send_task_assignment_email(instance)
        return

    # 2. Handle Task Updates
    if old_instance:
        # Check for status change
        if old_instance.status != instance.status:
            change_description = f"Status changed from '{old_instance.get_status_display()}' to '{instance.get_status_display()}'."
            TaskHistory.objects.create(
                task=instance,
                user=user,
                change_description=change_description,
                task_state=instance.to_dict()
            )
            # Notify creator and assignees of status change
            send_status_change_email(instance, old_instance.get_status_display())

        # Check for changes in assignees
        old_assignees = set(old_instance.assignees.all())
        new_assignees = set(instance.assignees.all())

        added_assignees = new_assignees - old_assignees
        removed_assignees = old_assignees - new_assignees

        if added_assignees:
            for assignee in added_assignees:
                change_description = f"User '{assignee.get_full_name()}' was assigned to the task."
                TaskHistory.objects.create(
                    task=instance,
                    user=user,
                    change_description=change_description,
                    task_state=instance.to_dict()
                )
            send_task_assignment_email(instance, added_assignees)

        if removed_assignees:
            for assignee in removed_assignees:
                change_description = f"User '{assignee.get_full_name()}' was unassigned from the task."
                TaskHistory.objects.create(
                    task=instance,
                    user=user,
                    change_description=change_description,
                    task_state=instance.to_dict()
                )

        # Status Adjustment on Reassignment
        if (added_assignees or removed_assignees) and \
           old_instance.status in [Task.StatusChoices.IN_PROGRESS, Task.StatusChoices.IN_REVIEW]:
            
            # Temporarily disconnect signal to prevent infinite loop
            post_save.disconnect(sender=Task, receiver=task_post_save)
            
            instance.status = Task.StatusChoices.TODO
            instance.save(update_fields=['status'])
            
            # Reconnect signal
            post_save.connect(sender=Task, receiver=task_post_save)

            # A new history entry and email for this status change will be created
            # when the signal is re-triggered by instance.save() above.

def send_task_assignment_email(task, assignees_to_notify=None):
    """
    Sends an email to assignees of a task.
    """
    if not assignees_to_notify:
        assignees_to_notify = task.assignees.all()

    subject = f"You have been assigned a new task: {task.title}"
    message = f"Hello,\n\nYou have been assigned to the task '{task.title}' in the project '{task.project.name}'.\n\nPlease review the task details."
    recipient_list = [assignee.email for assignee in assignees_to_notify if assignee.email]

    if recipient_list:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def send_status_change_email(task, old_status):
    """
    Sends an email when the status of a task changes.
    """
    subject = f"Task status updated: {task.title}"
    message = f"Hello,\n\nThe status of the task '{task.title}' has been updated from '{old_status}' to '{task.get_status_display()}'."
    
    # Notify the creator and all current assignees
    recipients = {task.creator.email} if task.creator and task.creator.email else set()
    for assignee in task.assignees.all():
        if assignee.email:
            recipients.add(assignee.email)

    if recipients:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(recipients))

# Add a to_dict method to the Task model for serialization

def task_to_dict(self):
    """
    Serializes the Task object to a dictionary.
    """
    return {
        'id': self.id,
        'title': self.title,
        'description': self.description,
        'status': self.status,
        'priority': self.priority,
        'assignees': [assignee.id for assignee in self.assignees.all()],
        'creator': self.creator.id if self.creator else None,
        'start_date': self.start_date.isoformat() if self.start_date else None,
        'due_date': self.due_date.isoformat() if self.due_date else None,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat(),
        'parent_task': self.parent_task.id if self.parent_task else None,
    }

Task.add_to_class('to_dict', task_to_dict)
