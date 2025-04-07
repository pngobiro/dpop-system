from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone # Added for date comparison
from django.contrib.contenttypes.fields import GenericRelation
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

        # Fallback return for the outer 'if overdue_tasks.exists()'
        # (Handles case where status is Overdue but no suitable task found)
        return None

    class Meta: # Correct indentation (aligned with method definitions)
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
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User assigned to this task"))
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User who created this task"))
    start_date = models.DateField(null=True, blank=True, help_text=_("Optional start date for the task")) # Added start_date
    due_date = models.DateField(null=True, blank=True, help_text=_("Optional due date for the task"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Generic relation to the Document model for task-level attachments
    if Document:
        attachments = GenericRelation(
            Document,
            content_type_field='content_type',
            object_id_field='object_id',
            related_query_name='task' # Keep this distinct from project's relation
        )

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    class Meta:
        ordering = ['project', 'start_date', 'due_date', 'priority', 'created_at'] # Correct ordering for Task
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


# Removed duplicate Task model definition
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
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User assigned to this task"))
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("User who created this task"))
    due_date = models.DateField(null=True, blank=True, help_text=_("Optional due date for the task"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Generic relation to the Document model for task-level attachments
    if Document:
        attachments = GenericRelation(
            Document,
            content_type_field='content_type',
            object_id_field='object_id',
            related_query_name='task' # Keep this distinct from project's relation
        )

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    class Meta:
        ordering = ['project', 'priority', 'due_date', 'created_at']
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
