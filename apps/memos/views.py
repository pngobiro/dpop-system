from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import (
    Memo, MemoType, MemoCategory, PriorityLevel, MemoStatus, 
    ActionItem, CommentThread, ThreadComment, MemoTimeline
)
from .forms import MemoForm, ActionItemForm, CommentThreadForm, ThreadCommentForm
from apps.document_management.models import Document
from apps.document_management.utils.document_manager import DocumentManager
from apps.tasks.forms import TaskForm
from apps.meetings.forms import MeetingForm

@login_required
def department_dashboard(request):
    """Department dashboard showing memo statistics and lists"""
    user = request.user
    department = user.department

    # Get memo statistics
    stats = {
        'total': Memo.objects.filter(department=department).count(),
        'physical': Memo.objects.filter(department=department, is_physical=True).count(),
        'digital': Memo.objects.filter(department=department, is_physical=False).count(),
        'confidential': Memo.objects.filter(department=department, is_confidential=True).count(),
        'my_memos': Memo.objects.filter(created_by=user).count(),
        'pending_actions': ActionItem.objects.filter(
            assigned_to=user,
            status__in=['pending', 'in_progress']
        ).count(),
    }

    # Recent memos
    recent_memos = Memo.objects.filter(
        Q(department=department) | Q(recipient_departments=department)
    ).distinct().order_by('-created_at')[:10]

    # Get memo types and categories for quick stats
    memo_types = MemoType.objects.filter(is_active=True).annotate(
        count=Count('memo', filter=Q(memo__department=department))
    )
    
    memo_categories = MemoCategory.objects.filter(is_active=True).annotate(
        count=Count('memo', filter=Q(memo__department=department))
    )

    context = {
        'stats': stats,
        'recent_memos': recent_memos,
        'memo_types': memo_types,
        'memo_categories': memo_categories,
        'segment': 'memos',  # Add segment for active navigation
    }
    return render(request, 'memos/dashboard.html', context)

    
@login_required
@login_required
def memo_create(request):
    """Create a new memo"""
    # Check if user has a department
    if not request.user.department:
        messages.error(request, 'You must be assigned to a department to create memos. Please contact the administrator.')
        return redirect('memos:dashboard')
    
    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, user=request.user, department=request.user.department)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.created_by = request.user
            memo.department = request.user.department
            
            # Set default status and priority if not set
            if not hasattr(memo, 'status') or not memo.status:
                memo.status = MemoStatus.objects.filter(name='Draft').first()
            if not hasattr(memo, 'priority') or not memo.priority:
                memo.priority = PriorityLevel.objects.filter(level=3).first()  # Medium priority
            
            memo.save()
            form.save_m2m()  # Save ManyToMany fields

            # Handle file attachments
            for file in request.FILES.getlist('attachments'):
                try:
                    document = DocumentManager.attach_document(
                        file=file,
                        source_object=memo,
                        uploaded_by=request.user,
                        title=f"Memo attachment - {memo.reference_number}",
                        is_confidential=memo.is_confidential
                    )
                    # Create MemoDocument link
                    from .models import MemoDocument
                    MemoDocument.objects.create(
                        memo=memo,
                        document=document,
                        document_type='attachment',
                        uploaded_by=request.user
                    )
                except Exception as e:
                    # Log the error but don't fail the memo creation
                    messages.warning(request, f'Failed to upload attachment "{file.name}": {str(e)}')

            # Create timeline entry
            MemoTimeline.objects.create(
                memo=memo,
                event_type='created',
                description=f'Memo created by {request.user.get_full_name()}',
                user=request.user
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Memo created successfully.'})
            messages.success(request, 'Memo created successfully.')
            return redirect('memos:memo_detail', pk=memo.pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = MemoForm(user=request.user, department=request.user.department)

    # Get available options for the form
    memo_types = MemoType.objects.filter(is_active=True)
    memo_categories = MemoCategory.objects.filter(is_active=True)
    priority_levels = PriorityLevel.objects.all()

    return render(request, 'memos/memo_form.html', {
        'form': form,
        'memo_types': memo_types,
        'memo_categories': memo_categories,
        'priority_levels': priority_levels,
        'action': 'Create',
        'segment': 'memos'
    })

    



@login_required
def memo_detail(request, pk):
    """View memo details"""
    memo = get_object_or_404(Memo, pk=pk)
    user = request.user

    # Check permissions
    if not (user == memo.created_by or 
            user.department == memo.department or
            memo.recipient_departments.filter(id=user.department.id).exists() or
            memo.recipient_users.filter(id=user.id).exists()):
        messages.error(request, "You don't have permission to view this memo.")
        return redirect('memos:department_dashboard')

    # Record view activity in timeline
    MemoTimeline.objects.create(
        memo=memo,
        event_type='view',
        description=f'Viewed by {user.get_full_name()}',
        user=user
    )

    # Get related data
    comment_threads = memo.comment_threads.all().order_by('-created_at')
    timeline_events = memo.timeline.all().order_by('-timestamp')[:20]
    action_items = memo.action_items.all().order_by('-created_at')
    documents = memo.documents.all().order_by('-uploaded_at')

    context = {
        'memo': memo,
        'comment_threads': comment_threads,
        'timeline_events': timeline_events,
        'action_items': action_items,
        'documents': documents,
        'comment_form': CommentThreadForm(),
        'can_edit': user == memo.created_by or user.has_perm('memos.change_memo'),
        'can_delete': user == memo.created_by or user.has_perm('memos.delete_memo'),
        'segment': 'memos',  # Add segment for active navigation
    }
    return render(request, 'memos/memo_detail.html', context)

@login_required
def create_task_from_memo(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user) # Pass user for form initialization
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.content_type = ContentType.objects.get_for_model(memo)
            task.object_id = memo.pk
            task.save()
            form.save_m2m() # Save ManyToMany fields like assignees

            MemoActivity.objects.create(
                memo=memo,
                user=request.user,
                action='create',
                action_details={'type': 'task', 'task_id': task.pk, 'task_title': task.title},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f'Task "{task.title}" created and linked to memo.')
            return redirect('memos:memo_detail', pk=memo.pk)
    else:
        # Pre-populate form with memo data
        initial_data = {
            'title': f'Task from Memo: {memo.title}',
            'description': f'Refer to memo {memo.reference_number}:\n\n{memo.content}',
            'due_date': memo.due_date,
            'priority': memo.priority,
            'project': memo.department.task_projects.first() if memo.department and memo.department.task_projects.exists() else None,
        }
        form = TaskForm(initial=initial_data, user=request.user)

    return render(request, 'memos/create_related_item.html', {
        'form': form,
        'memo': memo,
        'item_type': 'Task',
        'action_url': reverse('memos:create_task_from_memo', args=[memo.pk])
    })

@login_required
def create_meeting_from_memo(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        form = MeetingForm(request.POST, user=request.user) # Pass user for form initialization
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.organizer = request.user
            meeting.content_type = ContentType.objects.get_for_model(memo)
            meeting.object_id = memo.pk
            meeting.save()
            form.save_m2m() # Save ManyToMany fields like participants

            MemoActivity.objects.create(
                memo=memo,
                user=request.user,
                action='create',
                action_details={'type': 'meeting', 'meeting_id': meeting.pk, 'meeting_title': meeting.title},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f'Meeting "{meeting.title}" created and linked to memo.')
            return redirect('memos:memo_detail', pk=memo.pk)
    else:
        # Pre-populate form with memo data
        initial_data = {
            'title': f'Meeting for Memo: {memo.title}',
            'agenda': f'Discussion points from memo {memo.reference_number}:\n\n{memo.content}',
            'department': memo.department,
            'date': timezone.now().date(),
            'start_time': timezone.now().time(),
        }
        form = MeetingForm(initial=initial_data, user=request.user)

    return render(request, 'memos/create_related_item.html', {
        'form': form,
        'memo': memo,
        'item_type': 'Meeting',
        'action_url': reverse('memos:create_meeting_from_memo', args=[memo.pk])
    })

@login_required
@require_POST
def memo_submit(request, pk):
    """Submit memo for approval"""
    memo = get_object_or_404(Memo, pk=pk)
    
    if memo.created_by != request.user:
        messages.error(request, "You don't have permission to submit this memo.")
        return redirect('memos:memo_detail', pk=pk)

    if memo.status != 'draft':
        messages.error(request, "Only draft memos can be submitted for approval.")
        return redirect('memos:memo_detail', pk=pk)

    # Create approval workflow
    approvers = get_memo_approvers(memo)  # Define this function based on your workflow rules
    for level, approver in enumerate(approvers, 1):
        MemoApproval.objects.create(
            memo=memo,
            approver=approver,
            level=level
        )

    memo.status = 'pending_approval'
    memo.save()

    messages.success(request, 'Memo submitted for approval.')
    return redirect('memos:memo_detail', pk=pk)

@login_required
@require_POST
def memo_approve(request, pk):
    """Approve a memo"""
    memo = get_object_or_404(Memo, pk=pk)
    approval = get_object_or_404(
        MemoApproval, 
        memo=memo, 
        approver=request.user,
        status='pending'
    )

    approval.status = 'approved'
    approval.approved_at = timezone.now()
    approval.comments = request.POST.get('comments', '')
    approval.save()

    # Handle digital signature/stamp if provided
    if request.FILES.get('signature'):
        document = DocumentManager.attach_document(
            file=request.FILES['signature'],
            source_object=approval,
            uploaded_by=request.user,
            title=f"Approval signature - {memo.reference_number} - Level {approval.level}",
            is_confidential=memo.is_confidential
        )
        approval.signature_document = document
        approval.save()

    # Check if this was the final approval
    if not memo.approvals.filter(status='pending').exists():
        memo.status = 'approved'
        memo.save()
        messages.success(request, 'Final approval granted. Memo is now approved.')
    else:
        messages.success(request, 'Memo approved. Waiting for next level approval.')

    return redirect('memos:memo_detail', pk=pk)

@login_required
def pending_approvals(request):
    """List of memos pending user's approval"""
    pending = MemoApproval.objects.filter(
        approver=request.user,
        status='pending'
    ).select_related(
        'memo', 
        'memo__created_by', 
        'memo__department'
    ).order_by('memo__created_at')

    return render(request, 'memos/pending_approvals.html', {'approvals': pending})

@login_required
@require_POST
def add_comment(request, pk):
    """Add a comment to a memo"""
    memo = get_object_or_404(Memo, pk=pk)
    form = MemoCommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.memo = memo
        comment.user = request.user
        comment.save()

        # Handle attachments
        for file in request.FILES.getlist('attachments'):
            document = DocumentManager.attach_document(
                file=file,
                source_object=comment,
                uploaded_by=request.user,
                title=f"Comment attachment - {memo.reference_number}",
                is_confidential=memo.is_confidential
            )
            comment.attachments.add(document)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'comment_html': render_to_string(
                    'memos/partials/comment.html', 
                    {'comment': comment}
                )
            })

    messages.success(request, 'Comment added successfully.')
    return redirect('memos:memo_detail', pk=pk)

def get_memo_approvers(memo):
    """Helper function to determine memo approvers based on department hierarchy"""
    approvers = []
    department = memo.department

    # Add immediate supervisor
    if department.head:
        approvers.append(department.head)

    # Add department director
    if department.director and department.director != department.head:
        approvers.append(department.director)

    # Add additional approvers based on memo type and department
    if memo.memo_type == 'external':
        # Add any additional required approvers for external memos
        pass

    return approvers

@login_required
@login_required
def my_memos(request):
    """View for listing memos created by the current user with search and filter"""
    from apps.organization.models import Department
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    # Optimize query to include related data
    user_memos = Memo.objects.filter(created_by=request.user).select_related(
        'status', 'sender_internal', 'created_by', 'memo_type', 'category', 'priority'
    ).prefetch_related('documents__document')
    
    # Apply search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        user_memos = user_memos.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(reference_number__icontains=search_query) |
            Q(sender_external_name__icontains=search_query) |
            Q(sender_external_organization__icontains=search_query)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status')
    if status_filter:
        user_memos = user_memos.filter(status_id=status_filter)
    
    # Apply memo type filter
    memo_type_filter = request.GET.get('memo_type')
    if memo_type_filter:
        user_memos = user_memos.filter(memo_type_id=memo_type_filter)
    
    # Apply category filter
    category_filter = request.GET.get('category')
    if category_filter:
        user_memos = user_memos.filter(category_id=category_filter)
    
    # Apply priority filter
    priority_filter = request.GET.get('priority')
    if priority_filter:
        user_memos = user_memos.filter(priority_id=priority_filter)
    
    # Apply format filter (physical/digital)
    format_filter = request.GET.get('format')
    if format_filter == 'physical':
        user_memos = user_memos.filter(is_physical=True)
    elif format_filter == 'digital':
        user_memos = user_memos.filter(is_physical=False)
    
    # Apply attachments filter
    attachments_filter = request.GET.get('attachments')
    if attachments_filter == 'with':
        user_memos = user_memos.filter(documents__isnull=False).distinct()
    elif attachments_filter == 'without':
        user_memos = user_memos.filter(documents__isnull=True)
    
    # Apply date range filter
    date_range = request.GET.get('date_range')
    today = timezone.now().date()
    
    if date_range == 'today':
        user_memos = user_memos.filter(created_at__date=today)
    elif date_range == 'week':
        week_start = today - timedelta(days=today.weekday())
        user_memos = user_memos.filter(created_at__date__gte=week_start)
    elif date_range == 'month':
        month_start = today.replace(day=1)
        user_memos = user_memos.filter(created_at__date__gte=month_start)
    elif date_range == 'quarter':
        quarter_start = today.replace(month=((today.month - 1) // 3) * 3 + 1, day=1)
        user_memos = user_memos.filter(created_at__date__gte=quarter_start)
    elif date_range == 'year':
        year_start = today.replace(month=1, day=1)
        user_memos = user_memos.filter(created_at__date__gte=year_start)
    
    # Apply due date filter
    due_status = request.GET.get('due_status')
    if due_status == 'overdue':
        user_memos = user_memos.filter(due_date__lt=today)
    elif due_status == 'due_today':
        user_memos = user_memos.filter(due_date=today)
    elif due_status == 'due_week':
        week_end = today + timedelta(days=7)
        user_memos = user_memos.filter(due_date__gte=today, due_date__lte=week_end)
    elif due_status == 'no_due_date':
        user_memos = user_memos.filter(due_date__isnull=True)
    
    # Apply sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['title', '-title', 'created_at', '-created_at', 'due_date', '-due_date', 'status__name', '-status__name']:
        user_memos = user_memos.order_by(sort_by)
    else:
        user_memos = user_memos.order_by('-created_at')
    
    # Add pagination
    from django.core.paginator import Paginator
    paginator = Paginator(user_memos, 10)  # Show 10 memos per page
    page_number = request.GET.get('page')
    memos = paginator.get_page(page_number)
    
    # Get form and other data
    form = MemoForm(user=request.user, department=request.user.department)
    departments = Department.objects.filter(is_active=True)
    
    # Calculate statistics (based on unfiltered queryset for context)
    all_user_memos = Memo.objects.filter(created_by=request.user)
    total_memos = all_user_memos.count()
    
    draft_status = MemoStatus.objects.filter(name__icontains='draft').first()
    approved_status = MemoStatus.objects.filter(name__icontains='approved').first()
    pending_status = MemoStatus.objects.filter(name__icontains='pending').first()
    
    total_draft = all_user_memos.filter(status=draft_status).count() if draft_status else 0
    total_approved = all_user_memos.filter(status=approved_status).count() if approved_status else 0
    total_pending = all_user_memos.filter(status=pending_status).count() if pending_status else 0
    total_physical = all_user_memos.filter(is_physical=True).count()
    total_confidential = all_user_memos.filter(is_confidential=True).count()
    
    # Get filter options
    memo_types = MemoType.objects.filter(is_active=True)
    memo_categories = MemoCategory.objects.filter(is_active=True)
    memo_statuses = MemoStatus.objects.filter(is_active=True)
    priority_levels = PriorityLevel.objects.all()
    
    return render(request, 'memos/my_memos.html', {
        'memos': memos,
        'form': form,
        'departments': departments,
        'memo_types': memo_types,
        'memo_categories': memo_categories,
        'memo_statuses': memo_statuses,
        'priority_levels': priority_levels,
        'total_memos': total_memos,
        'total_draft': total_draft,
        'total_pending': total_pending,
        'total_approved': total_approved,
        'total_physical': total_physical,
        'total_confidential': total_confidential,
        'today': today,
        'segment': 'memos',
    })



@login_required
def memo_edit(request, pk):
    """Edit an existing memo"""
    memo = get_object_or_404(Memo, pk=pk)

    # Check if memo can be edited (only draft status or user has permission)
    draft_status = MemoStatus.objects.filter(name__icontains='draft').first()
    if memo.status != draft_status and not request.user.has_perm('memos.change_memo'):
        messages.error(request, "Only draft memos can be edited.")
        return redirect('memos:memo_detail', pk=pk)

    # Check permissions
    if not (request.user == memo.created_by or request.user.has_perm('memos.change_memo')):
        messages.error(request, "You don't have permission to edit this memo.")
        return redirect('memos:memo_detail', pk=pk)

    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, instance=memo, user=request.user, department=request.user.department)
        if form.is_valid():
            memo = form.save()
            form.save_m2m()
            
            # Handle file attachments
            for file in request.FILES.getlist('attachments'):
                try:
                    document = DocumentManager.attach_document(
                        file=file,
                        source_object=memo,
                        uploaded_by=request.user,
                        title=f"Memo attachment - {memo.reference_number}",
                        is_confidential=memo.is_confidential
                    )
                    # Create MemoDocument link
                    from .models import MemoDocument
                    MemoDocument.objects.create(
                        memo=memo,
                        document=document,
                        document_type='attachment',
                        uploaded_by=request.user
                    )
                except Exception as e:
                    # Log the error but don't fail the memo update
                    messages.warning(request, f'Failed to upload attachment "{file.name}": {str(e)}')
            
            # Record edit in timeline
            MemoTimeline.objects.create(
                memo=memo,
                event_type='update',
                description=f'Memo updated by {request.user.get_full_name()}',
                user=request.user
            )
            
            messages.success(request, 'Memo updated successfully.')
            return redirect('memos:memo_detail', pk=memo.pk)
    else:
        form = MemoForm(instance=memo, user=request.user, department=request.user.department)

    # Get available options
    memo_types = MemoType.objects.filter(is_active=True)
    memo_categories = MemoCategory.objects.filter(is_active=True)
    priority_levels = PriorityLevel.objects.all()

    return render(request, 'memos/memo_form.html', {
        'form': form,
        'memo_types': memo_types,
        'memo_categories': memo_categories,
        'priority_levels': priority_levels,
        'memo': memo,
        'action': 'Edit'
    })

    return render(request, 'memos/memo_form.html', {
        'form': form,
        'memo': memo,
        'templates': templates,
        'action': 'Edit'
    })


@login_required
@require_POST
def memo_delete(request, pk):
    """Delete a memo"""
    memo = get_object_or_404(Memo, pk=pk)
    
    # Check permissions
    if not (request.user == memo.created_by or request.user.has_perm('memos.delete_memo')):
        messages.error(request, "You don't have permission to delete this memo.")
        return redirect('memos:memo_detail', pk=pk)
    
    if request.method == 'POST':
        memo_ref = memo.reference_number
        memo.delete()
        messages.success(request, f'Memo {memo_ref} deleted successfully.')
        return redirect('memos:my_memos')
    
    return render(request, 'memos/memo_confirm_delete.html', {'memo': memo})


@login_required
def create_task_from_memo(request, pk):
    """Create a task from a memo"""
    memo = get_object_or_404(Memo, pk=pk)
    
    if request.method == 'POST':
        # Create action item from memo
        action_item = ActionItem.objects.create(
            memo=memo,
            title=f"Action from {memo.reference_number}",
            description=memo.subject,
            assigned_to=request.user,
            assigned_by=request.user,
            priority=memo.priority,
            due_date=memo.due_date
        )
        
        # Record in timeline
        MemoTimeline.objects.create(
            memo=memo,
            event_type='action_created',
            description=f'Action item created: {action_item.title}',
            user=request.user
        )
        
        messages.success(request, 'Action item created from memo.')
        return redirect('memos:memo_detail', pk=pk)
    
    return render(request, 'memos/create_task_from_memo.html', {'memo': memo})


@login_required
def create_meeting_from_memo(request, pk):
    """Create a meeting from a memo"""
    memo = get_object_or_404(Memo, pk=pk)
    
    if request.method == 'POST':
        # This would integrate with your meetings app
        # For now, just create a timeline entry
        MemoTimeline.objects.create(
            memo=memo,
            event_type='meeting_scheduled',
            description=f'Meeting scheduled regarding {memo.reference_number}',
            user=request.user
        )
        
        messages.success(request, 'Meeting request created from memo.')
        return redirect('memos:memo_detail', pk=pk)
    
    return render(request, 'memos/create_meeting_from_memo.html', {'memo': memo})


@login_required
@require_POST
def add_comment(request, pk):
    """Add a comment thread to a memo"""
    memo = get_object_or_404(Memo, pk=pk)
    
    # Check permissions
    if not (request.user == memo.created_by or 
            request.user.department == memo.department or
            memo.recipient_departments.filter(id=request.user.department.id).exists() or
            memo.recipient_users.filter(id=request.user.id).exists()):
        messages.error(request, "You don't have permission to comment on this memo.")
        return redirect('memos:memo_detail', pk=pk)
    
    thread_form = CommentThreadForm(request.POST)
    comment_form = ThreadCommentForm(request.POST)
    
    if thread_form.is_valid() and comment_form.is_valid():
        # Create thread
        thread = thread_form.save(commit=False)
        thread.memo = memo
        thread.created_by = request.user
        thread.save()
        
        # Create first comment
        comment = comment_form.save(commit=False)
        comment.thread = thread
        comment.author = request.user
        comment.save()
        
        # Record in timeline
        MemoTimeline.objects.create(
            memo=memo,
            event_type='comment_added',
            description=f'Comment added by {request.user.get_full_name()}',
            user=request.user
        )
        
        messages.success(request, 'Comment added successfully.')
    else:
        messages.error(request, 'Error adding comment.')
    
    return redirect('memos:memo_detail', pk=pk)

@login_required
@require_POST
def memo_status_update(request, pk):
    """Update memo status via AJAX"""
    memo = get_object_or_404(Memo, pk=pk)
    
    # Check permissions
    if not (request.user == memo.created_by or 
            request.user.department == memo.department or
            request.user.has_perm('memos.change_memo')):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        new_status_id = request.POST.get('status_id')
        new_status = MemoStatus.objects.get(id=new_status_id)
        old_status = memo.status
        
        memo.status = new_status
        memo.save()
        
        # Record status change in timeline
        MemoTimeline.objects.create(
            memo=memo,
            event_type='status_changed',
            description=f'Status changed from {old_status.name if old_status else "None"} to {new_status.name}',
            user=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Status updated to {new_status.name}',
            'new_status': new_status.name,
            'new_status_color': new_status.color
        })
        
    except MemoStatus.DoesNotExist:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def memo_attachments(request, pk):
    """Get memo attachments via AJAX"""
    memo = get_object_or_404(Memo, pk=pk)
    
    # Check permissions
    if not (request.user == memo.created_by or 
            request.user.department == memo.department or
            memo.recipient_departments.filter(id=request.user.department.id).exists() or
            memo.recipient_users.filter(id=request.user.id).exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        documents = memo.documents.all()
        data = {
            'documents': [
                {
                    'id': doc.document.id,
                    'title': doc.document.title,
                    'document_type': doc.document_type,
                    'uploaded_at': doc.uploaded_at.isoformat(),
                    'uploaded_by': doc.uploaded_by.get_full_name(),
                    'download_url': doc.document.get_download_url() if hasattr(doc.document, 'get_download_url') else '#'
                }
                for doc in documents
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


