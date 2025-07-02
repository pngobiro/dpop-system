from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from authentication.models import CustomUser
from apps.tasks.models import Task, Project
from apps.meetings.models import Meeting
from apps.document_management.models import Document
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime # Import datetime module

try:
    from apps.organization.models import Department
except ImportError:
    Department = None


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'tasks/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        if not Department:
            # Handle case where Department model is not available
            return Department.objects.none() # Return an empty queryset
        return Department.objects.all().order_by('name')


def _get_task_statistics(task_queryset):
    """
    Calculates and returns a dictionary of task statistics for a given queryset.
    """
    stats = {
        'total': task_queryset.count(),
        'TODO': task_queryset.filter(status=Task.StatusChoices.TODO).count(),
        'IN_PROGRESS': task_queryset.filter(status=Task.StatusChoices.IN_PROGRESS).count(),
        'DONE': task_queryset.filter(status=Task.StatusChoices.DONE).count(),
        'BLOCKED': task_queryset.filter(status=Task.StatusChoices.BLOCKED).count(),
        'APPROVED': task_queryset.filter(status=Task.StatusChoices.APPROVED).count(),
        'REJECTED': task_queryset.filter(status=Task.StatusChoices.REJECTED).count(),
        'IN_REVIEW': task_queryset.filter(status=Task.StatusChoices.IN_REVIEW).count(),
        'ON_HOLD': task_queryset.filter(status=Task.StatusChoices.ON_HOLD).count(),
    }
    return stats


@login_required
def user_tasks_dashboard(request):
    """Dashboard showing user's tasks"""
    today = timezone.now().date()
    
    # Get tasks assigned to the user
    assigned_tasks = Task.objects.filter(assignees=request.user).select_related('project').prefetch_related('assignees').order_by('due_date')
    
    # Tasks created by the user
    created_tasks = Task.objects.filter(creator=request.user).select_related('project').order_by('due_date')
    
    # Pending tasks (not done)
    pending_tasks = assigned_tasks.exclude(status=Task.StatusChoices.DONE)
    
    # Overdue tasks
    overdue_tasks = pending_tasks.filter(due_date__lt=today)
    
    # Tasks due today
    due_today = pending_tasks.filter(due_date=today)
    
    # Recently completed tasks
    completed_tasks = assigned_tasks.filter(
        status=Task.StatusChoices.DONE
    ).order_by('-updated_at')[:5]
    
    context = {
        'assigned_tasks': assigned_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'due_today': due_today,
        'completed_tasks': completed_tasks,
        'created_tasks': created_tasks,
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required
def my_dashboard(request):
    """Dashboard showing user's tasks, meetings, and documents"""
    today = timezone.now().date()
    
    # Get tasks assigned to me with detailed stats
    my_tasks_queryset = Task.objects.filter(assignees=request.user)
    my_tasks_stats = _get_task_statistics(my_tasks_queryset)
    
    # Get tasks I assigned to others
    tasks_i_assigned_queryset = Task.objects.filter(creator=request.user)
    assigned_tasks_stats = _get_task_statistics(tasks_i_assigned_queryset)
    
    # Get meetings stats
    all_meetings = Meeting.objects.all()
    meetings_stats = {
        'upcoming': Meeting.objects.filter(date__gte=today).count(),
        'today': Meeting.objects.filter(date=today).count(),
        'this_week': Meeting.objects.filter(date__gte=today, date__lte=today + timezone.timedelta(days=7)).count()
    }
    
    # Get document count
    document_count = Document.objects.count() if Document else 0
    
    context = {
        'my_tasks_stats': my_tasks_stats,
        'assigned_tasks_stats': assigned_tasks_stats,
        'meetings_stats': meetings_stats,
        'document_count': document_count,
        'segment': 'my_dashboard' # Add segment for active navigation
    }
    return render(request, 'tasks/my_dashboard.html', context)


@login_required
def tasks_assigned_by_me(request):
    """View for tasks that are assigned to the current user"""
    # Retrieve tasks assigned to the current user
    tasks_assigned_to_me_queryset = Task.objects.filter(
        assignees=request.user
    ).select_related(
        'project'
    ).prefetch_related(
        'assignees'
    ).order_by(
        'status',  # Order by status first
        '-due_date',  # Then by due date (most recent first)
        '-created_at'  # Then by creation date
    )

    # Calculate statistics using the helper function
    assigned_tasks_stats = _get_task_statistics(tasks_assigned_to_me_queryset)

    # Retrieve all active users for the assign task modal (excluding current user)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()
    meetings = Meeting.objects.all() # Fetch all meetings

    context = {
        'tasks': tasks_assigned_to_me_queryset, # Pass tasks assigned to the user
        'title': 'Tasks Assigned to Me', # Page title
        'users': users,
        'projects': projects,
        'meetings': meetings, # Pass meetings to the template
        'request': request,
        'assigned_tasks_stats': assigned_tasks_stats, # Pass the calculated stats
    }
    return render(request, 'tasks/tasks_assigned.html', context)


@login_required
def tasks_created_by_me(request):
    """View for tasks that the user has created"""
    # Retrieve tasks created by the current user
    tasks_created_by_me_queryset = Task.objects.filter(
        creator=request.user
    ).select_related(
        'project'
    ).prefetch_related(
        'assignees'
    ).order_by(
        'status',  # Order by status first
        '-due_date',  # Then by due date (most recent first)
        '-created_at'  # Then by creation date
    )

    # Calculate statistics using the helper function
    created_tasks_stats = _get_task_statistics(tasks_created_by_me_queryset)

    # Retrieve all active users for the assign task modal (excluding current user)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()

    context = {
        'tasks': tasks_created_by_me_queryset, # Pass tasks created by the user
        'title': 'Tasks I Assigned', # Page title
        'users': users,
        'projects': projects,
        'request': request,
        'assigned_tasks_stats': created_tasks_stats, # Pass the calculated stats (using assigned_tasks_stats key for template compatibility)
    }
    return render(request, 'tasks/tasks_assigned.html', context)


@login_required
def assign_task(request):
    """Handle assigning a new task"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignee_ids = request.POST.getlist('assignees[]')
        due_date_str = request.POST.get('due_date')
        project_id = request.POST.get('project')
        related_meeting_id = request.POST.get('related_meeting')
        files = request.FILES.getlist('attachments[]')

        # Validate required fields
        if not all([title, description, due_date_str, project_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('tasks:tasks_assigned_by_me')

        try:
            project = Project.objects.get(id=project_id)
            
            # --- Permission Check for Task Assignment ---
            can_assign = False
            # 1. Global Administrator
            if request.user.is_superuser or request.user.is_staff:
                can_assign = True
            # 2. Project Owner (can assign tasks within their project)
            elif request.user == project.owner:
                can_assign = True
            # 3. Department Head/Manager (can assign tasks within their department)
            elif request.user.department and project.department and \
                 request.user.department == project.department and \
                 (request.user.is_director or request.user.is_manager):
                can_assign = True
            # 4. Task Creator (implicitly allowed to assign the task they are creating)
            # This is handled by the fact that request.user is the creator of the new task.
            # No explicit check needed here as the task is not yet created.

            if not can_assign:
                messages.error(request, "You do not have permission to assign tasks in this project or department.")
                return redirect('tasks:tasks_assigned_by_me')

            # Convert due_date string to date object
            try:
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                messages.error(request, 'Invalid due date format.')
                return redirect('tasks:tasks_assigned_by_me')

            # Create the base task
            task = Task.objects.create(
                project=project,
                title=title,
                description=description,
                creator=request.user,
                due_date=due_date
            )

            # Handle related meeting
            if related_meeting_id:
                try:
                    related_meeting = Meeting.objects.get(id=related_meeting_id)
                    task.content_type = ContentType.objects.get_for_model(related_meeting)
                    task.object_id = related_meeting.pk
                    task.save(update_fields=['content_type', 'object_id'])
                except Meeting.DoesNotExist:
                    messages.warning(request, "Related meeting not found.")
                except Exception as e:
                    messages.error(request, f"Error linking task to meeting: {e}")

            # Handle assignees
            assigned_users = []

            # Add other assignees
            for assignee_id in assignee_ids:
                try:
                    assignee = CustomUser.objects.get(id=assignee_id)
                    task.assignees.add(assignee)
                    assigned_users.append(assignee.get_full_name() or assignee.username)
                except CustomUser.DoesNotExist:
                    messages.warning(request, f'User with ID {assignee_id} not found.')

            # Always add current user if they're not already in the assignees
            # This logic assumes the "Assign to myself" checkbox is handled client-side
            # and its value is reflected in assignee_ids if checked.
            # If not, you might need to explicitly add request.user here based on a separate form field.
            # For now, assuming assignee_ids will contain request.user.id if "Assign to myself" is checked.
            if request.POST.get('assign_to_self') == 'on': # Checkbox value is 'on' if checked
                if str(request.user.id) not in assignee_ids: # Only add if not already selected in multi-select
                    task.assignees.add(request.user)
                    assigned_users.append(request.user.get_full_name() or request.user.username)


            # Handle file attachments using Google Drive
            from apps.document_management.utils.google_drive_manager import GoogleDriveManager
            drive_manager = GoogleDriveManager()
            
            for file in files:
                if file.size <= 10 * 1024 * 1024:  # 10MB limit
                    try:
                        # Get or create Tasks folder
                        tasks_folder_name = 'Tasks'
                        tasks_folder = drive_manager.service.files().list(
                            q=f"name='{tasks_folder_name}' and mimeType='application/vnd.google-apps.folder' and '{drive_manager.DEFAULT_FOLDER_ID}' in parents",
                            fields='files(id, name)',
                            supportsAllDrives=True,
                            includeItemsFromAllDrives=True
                        ).execute()

                        if not tasks_folder.get('files'):
                            tasks_folder_id = drive_manager.create_folder(tasks_folder_name, drive_manager.DEFAULT_FOLDER_ID)
                        else:
                            tasks_folder_id = tasks_folder['files'][0]['id']

                        # Upload file to Google Drive
                        filename = f"Task_{task.id}_{task.title[:20]}_{file.name}"
                        file_id, web_link = drive_manager.upload_file(
                            file_obj=file,
                            filename=filename,
                            folder_id=tasks_folder_id
                        )
                        
                        if file_id and web_link:
                            Document.objects.create(
                                title=file.name,
                                file_type=file.content_type,
                                file_size=file.size,
                                storage_type='google_drive',
                                drive_file_id=file_id,
                                drive_view_link=web_link,
                                content_type=ContentType.objects.get_for_model(task),
                                object_id=task.id,
                                source_module='tasks',
                                uploaded_by=request.user,
                                description=f"Attachment for Task: {task.title}"
                            )
                    except Exception as e:
                        messages.error(request, f'Error uploading file {file.name}: {str(e)}')
                else:
                    messages.warning(request, f'File {file.name} exceeds 10MB limit and was not uploaded.')

            # Success message
            assignee_list = ", ".join(assigned_users)
            attachment_count = len([f for f in files if f.size <= 10 * 1024 * 1024])
            messages.success(
                request,
                f'Task "{title}" has been successfully assigned to {assignee_list}. '
                f'Due date: {task.due_date.strftime("%B %d, %Y")}. '
                f'{attachment_count} file(s) attached.'
            )

        except Project.DoesNotExist:
            messages.error(request, 'Selected project does not exist.')
        except ValueError as ve:
            messages.error(request, f'Invalid data provided: {str(ve)}')
        except Exception as e:
            messages.error(request, f'Error assigning task: {str(e)}')

    return redirect('tasks:tasks_assigned_by_me')