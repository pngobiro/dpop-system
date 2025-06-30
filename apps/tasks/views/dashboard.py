from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from authentication.models import CustomUser
from apps.tasks.models import Task, Project
from apps.meetings.models import Meeting
from apps.document_management.models import Document

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
    my_tasks = Task.objects.filter(assignees=request.user)
    my_tasks_stats = {
        'total': my_tasks.count(),
        'pending': my_tasks.exclude(status=Task.StatusChoices.DONE).count(),
        'completed': my_tasks.filter(status=Task.StatusChoices.DONE).count(),
        'overdue': my_tasks.exclude(status=Task.StatusChoices.DONE).filter(due_date__lt=today).count(),
        'due_today': my_tasks.exclude(status=Task.StatusChoices.DONE).filter(due_date=today).count()
    }
    
    # Get tasks I assigned to others
    tasks_i_assigned = Task.objects.filter(creator=request.user)
    assigned_tasks_stats = {
        'total': tasks_i_assigned.count(),
        'pending': tasks_i_assigned.exclude(status=Task.StatusChoices.DONE).count(),
        'completed': tasks_i_assigned.filter(status=Task.StatusChoices.DONE).count()
    }
    
    # Get meetings stats
    all_meetings = Meeting.objects.all()
    meetings_stats = {
        'upcoming': Meeting.objects.filter(date__gte=today).count(),
        'today': Meeting.objects.filter(date=today).count(),
        'this_week': Meeting.objects.filter(date__gte=today, date__lte=today + timezone.timedelta(days=7)).count()
    }
    
    context = {
        'my_tasks_stats': my_tasks_stats,
        'assigned_tasks_stats': assigned_tasks_stats,
        'meetings_stats': meetings_stats,
        'document_count': 0, #Document.objects.count()
        'segment': 'my_dashboard' # Add segment for active navigation
    }
    return render(request, 'tasks/my_dashboard.html', context)


@login_required
def tasks_assigned_by_me(request):
    """View for tasks that are assigned to the current user"""
    # Get tasks assigned to the user
    tasks_assigned_to_me = Task.objects.filter(
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

    # Calculate statistics for tasks assigned to the user
    assigned_tasks_stats = {
        'total': tasks_assigned_to_me.count(),
        'TODO': tasks_assigned_to_me.filter(status=Task.StatusChoices.TODO).count(),
        'IN_PROGRESS': tasks_assigned_to_me.filter(status=Task.StatusChoices.IN_PROGRESS).count(),
        'DONE': tasks_assigned_to_me.filter(status=Task.StatusChoices.DONE).count(),
        'BLOCKED': tasks_assigned_to_me.filter(status=Task.StatusChoices.BLOCKED).count(),
        'APPROVED': tasks_assigned_to_me.filter(status=Task.StatusChoices.APPROVED).count(),
        'REJECTED': tasks_assigned_to_me.filter(status=Task.StatusChoices.REJECTED).count(),
        'REASSIGNED': tasks_assigned_to_me.filter(status=Task.StatusChoices.REASSIGNED).count(),
        'IN_REVIEW': tasks_assigned_to_me.filter(status=Task.StatusChoices.IN_REVIEW).count(),
        'ON_HOLD': tasks_assigned_to_me.filter(status=Task.StatusChoices.ON_HOLD).count(),
    }


    # Get all users for the assign task modal (still needed for the modal)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()

    context = {
        'tasks': tasks_assigned_to_me, # Pass tasks assigned to the user
        'title': 'Tasks Assigned to Me', # Revert title
        'users': users,
        'projects': projects,
        'request': request,
        'assigned_tasks_stats': assigned_tasks_stats, # Pass the calculated stats
    }
    return render(request, 'tasks/tasks_assigned.html', context)


    return render(request, 'tasks/tasks_assigned.html', context)


@login_required
def tasks_created_by_me(request):
    """View for tasks that the user has created"""
    # Get tasks created by the user
    tasks_created_by_me = Task.objects.filter(
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

    # Calculate statistics for tasks created by the user
    created_tasks_stats = {
        'total': tasks_created_by_me.count(),
        'TODO': tasks_created_by_me.filter(status=Task.StatusChoices.TODO).count(),
        'IN_PROGRESS': tasks_created_by_me.filter(status=Task.StatusChoices.IN_PROGRESS).count(),
        'DONE': tasks_created_by_me.filter(status=Task.StatusChoices.DONE).count(),
        'BLOCKED': tasks_created_by_me.filter(status=Task.StatusChoices.BLOCKED).count(),
        'APPROVED': tasks_created_by_me.filter(status=Task.StatusChoices.APPROVED).count(),
        'REJECTED': tasks_created_by_me.filter(status=Task.StatusChoices.REJECTED).count(),
        'REASSIGNED': tasks_created_by_me.filter(status=Task.StatusChoices.REASSIGNED).count(),
        'IN_REVIEW': tasks_created_by_me.filter(status=Task.StatusChoices.IN_REVIEW).count(),
        'ON_HOLD': tasks_created_by_me.filter(status=Task.StatusChoices.ON_HOLD).count(),
    }

    # Get all users for the assign task modal (still needed for the modal)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()

    context = {
        'tasks': tasks_created_by_me, # Pass tasks created by the user
        'title': 'Tasks I Assigned', # Title for this page
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
        due_date = request.POST.get('due_date')
        project_id = request.POST.get('project')
        files = request.FILES.getlist('attachments[]')

        # Check required fields, but allow empty assignees if self-assigning
        if not all([title, description, due_date, project_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('tasks:tasks_assigned_by_me')

        try:
            project = Project.objects.get(id=project_id)

            # Create the base task
            task = Task.objects.create(
                project=project,
                title=title,
                description=description,
                creator=request.user,
                due_date=due_date
            )

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
            if request.user not in task.assignees.all():
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