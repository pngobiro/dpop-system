from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone # Added for date comparison
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Using the custom user model specified in settings
User = settings.AUTH_USER_MODEL

# Import Document model safely
try:
    from apps.document_management.models import Document
except ImportError:
    Document = None

# Import Department model safely
try:
    from apps.organization.models import Department
except ImportError:
    Department = None

class Project(models.Model):
    """
    Represents a project which groups related tasks.
    Can be linked to a specific department and have attachments.
    """
    name = models.CharField(max_length=255, unique=True, help_text=_("Name of the project"))
    description = models.TextField(blank=True, null=True, help_text=_("Optional description of the project"))
    owner = models.ForeignKey(User, related_name='owned_projects', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User who owns/created the project"))
    department = models.ForeignKey(
        Department,
        related_name='task_projects',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Optional department this project belongs to")
    ) if Department else None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Generic relation to the Document model for project-level attachments
    if Document:
        attachments = GenericRelation(
            Document,
            content_type_field='content_type',
            object_id_field='object_id',
            related_query_name='project' # How to refer back from Document to Project
        )

    def __str__(self):
        if self.department:
            return f"{self.name} ({self.department.name})"
        return self.name

    def get_status(self):
        """
        Calculates the overall status of the project based on its tasks.
        """
        tasks = self.tasks.all()
        if not tasks.exists():
            return "Pending" # No tasks yet

        all_done = all(task.status == Task.StatusChoices.DONE for task in tasks)
        if all_done:
            return "Completed"

        today = timezone.now().date()
        is_overdue = any(task.due_date and task.due_date < today and task.status != Task.StatusChoices.DONE for task in tasks)
        if is_overdue:
            return "Overdue"

        return "In Progress" # Has tasks, not all done, none overdue

    def get_overdue_days(self):
        """
        If the project status is 'Overdue', calculates how many days
        the most overdue task is past its due date.
        Returns None otherwise.
        """
        if self.get_status() != "Overdue":
            return None

        today = timezone.now().date()
        oldest_due_date = None

        # Find the oldest past due date among non-DONE tasks
        overdue_tasks = self.tasks.filter(
            due_date__isnull=False,
            due_date__lt=today
        ).exclude(status=Task.StatusChoices.DONE).order_by('due_date')

        if overdue_tasks.exists():
            oldest_task = overdue_tasks.first()
            return (today - oldest_task.due_date).days

        # Fallback return
        return None

    class Meta:
        ordering = ['department__name', 'name']
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class Task(models.Model):
    """
    Represents a single task within a project. Can have attachments.
    """
    class StatusChoices(models.TextChoices):
        TODO = 'TODO', _('To Do')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        DONE = 'DONE', _('Done')
        BLOCKED = 'BLOCKED', _('Blocked')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        
        IN_REVIEW = 'IN_REVIEW', _('In Review')
        ON_HOLD = 'ON_HOLD', _('On Hold')

    class PriorityChoices(models.IntegerChoices):
        LOW = 1, _('Low')
        MEDIUM = 2, _('Medium')
        HIGH = 3, _('High')
        URGENT = 4, _('Urgent')

    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, help_text=_("The project this task belongs to"))
    title = models.CharField(max_length=255, help_text=_("Title of the task"))
    description = models.TextField(blank=True, null=True, help_text=_("Detailed description of the task"))
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.TODO,
        help_text=_("Current status of the task")
    )
    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        help_text=_("Priority level of the task")
    )
    assignees = models.ManyToManyField(
        User,
        related_name='tasks_assigned',
        blank=True,
        help_text=_("Users assigned to this task")
    )
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User who created this task"))
    start_date = models.DateField(null=True, blank=True, help_text=_("Optional start date for the task"))
    due_date = models.DateField(null=True, blank=True, help_text=_("Optional due date for the task"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_task = models.ForeignKey('self', null=True, blank=True, related_name='subtasks', on_delete=models.CASCADE)

    # Fields for Generic Relation to a source object (e.g., Meeting, Memo)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL, # Or models.CASCADE, depending on desired behavior
        null=True,
        blank=True,
        help_text="The content type of the object this task is related to (e.g., Meeting, Memo)."
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="The ID of the related object."
    )
    # This is the GenericForeignKey itself, providing easy access to the related object
    source_object = GenericForeignKey('content_type', 'object_id')

    # Generic relation to the Document model for task-level attachments
    if Document:
        attachments = GenericRelation(
            Document,
            content_type_field='content_type',
            object_id_field='object_id',
            related_query_name='task'
        )

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    class Meta:
        ordering = ['project', 'start_date', 'due_date', 'priority', 'created_at']
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


class Comment(models.Model):
    """
    Represents a comment made on a task.
    """
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE, help_text=_("The task this comment belongs to"))
    author = models.ForeignKey(User, related_name='task_comments', on_delete=models.CASCADE, help_text=_("User who wrote the comment"))
    content = models.TextField(help_text=_("The content of the comment"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task.title} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

class TaskHistory(models.Model):
    """
    Represents a history entry for a task, tracking changes to its status,
    assignees, or other important fields.
    """
    task = models.ForeignKey('Task', related_name='history', on_delete=models.CASCADE, help_text=_("The task this history entry belongs to"))
    user = models.ForeignKey(User, related_name='task_history', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User who made the change"))
    timestamp = models.DateTimeField(auto_now_add=True, help_text=_("Timestamp of the change"))
    change_description = models.CharField(max_length=255, help_text=_("A human-readable description of the change."), default='')
    # Store the complete task state as a JSON
    task_state = models.JSONField(help_text=_("The complete state of the task at this point in time"))
    comment = models.TextField(blank=True, null=True, help_text=_("Optional comment describing the change"))

    def __str__(self):
        return f"History for {self.task.title} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Task History")
        verbose_name_plural = _("Task Histories")
