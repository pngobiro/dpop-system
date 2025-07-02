from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Memo, MemoTemplate, MemoApproval, MemoComment, MemoActivity
from .forms import MemoForm, MemoTemplateForm, MemoCommentForm
from apps.document_management.models import Document
from apps.document_management.utils.document_manager import DocumentManager

@login_required
def department_dashboard(request):
    """Department dashboard showing memo statistics and lists"""
    user = request.user
    department = user.department

    # Get memos statistics
    stats = {
        'draft': Memo.objects.filter(department=department, status='draft').count(),
        'pending': Memo.objects.filter(department=department, status='pending_approval').count(),
        'approved': Memo.objects.filter(department=department, status='approved').count(),
        'published': Memo.objects.filter(department=department, status='published').count(),
        'my_memos': Memo.objects.filter(created_by=user).count()
    }

    # Recent memos
    recent_memos = Memo.objects.filter(
        Q(department=department) | Q(recipient_departments=department)
    ).distinct().order_by('-created_at')[:10]

    # Pending approvals
    pending_approvals = MemoApproval.objects.filter(
        approver=request.user,
        status='pending'
    ).select_related('memo').order_by('memo__created_at')

    context = {
        'stats': stats,
        'recent_memos': recent_memos,
        'pending_approvals': pending_approvals
    }
    return render(request, 'memos/dashboard.html', context)

    
@login_required
def memo_create(request):
    """Create a new memo"""
    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, user=request.user)  # Pass user to the form
        if form.is_valid():
            memo = form.save(commit=False)
            memo.created_by = request.user
            memo.department = request.user.department
            if not memo.sender_user: # If sender_user is not explicitly set in the form, default to the creator
                memo.sender_user = request.user
            memo.save()
            form.save_m2m()  # Save ManyToMany fields

            # Handle document creation if file is uploaded
            if request.FILES.get('document'):
                memo.create_document(request.FILES['document'])

            messages.success(request, 'Memo created successfully.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Memo created successfully.'})
            return redirect('memos:memo_detail', pk=memo.pk)
    else:
        form = MemoForm(user=request.user) # Pass the user to the form!

    templates = MemoTemplate.objects.filter(
        Q(department=request.user.department) | Q(department__isnull=True)
    )

    return render(request, 'memos/memo_form.html', {
        'form': form,
        'templates': templates,
        'action': 'Create'  # Add action for dynamic text
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

    # Record view activity
    MemoActivity.objects.create(
        memo=memo,
        user=user,
        action='view',
        ip_address=request.META.get('REMOTE_ADDR')
    )

    context = {
        'memo': memo,
        'approvals': memo.approvals.select_related('approver').order_by('level'),
        'comments': memo.comments.select_related('user').order_by('created_at'),
        'activities': memo.activities.select_related('user').order_by('-timestamp')[:10],
        'can_approve': MemoApproval.objects.filter(
            memo=memo, 
            approver=user, 
            status='pending'
        ).exists(),
        'memo_status_choices': Memo.MEMO_STATUS,
        'memo_priority_choices': Memo.PRIORITY_CHOICES,
    }
    return render(request, 'memos/memo_detail.html', context)

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
def my_memos(request):
    """View for listing memos created by the current user"""
    memos = Memo.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'memos/my_memos.html', {'memos': memos})



@login_required
def memo_edit(request, pk):
    """Edit an existing memo"""
    memo = get_object_or_404(Memo, pk=pk)

    if memo.status != 'draft':
        messages.error(request, "Only draft memos can be edited.")
        return redirect('memos:memo_detail', pk=pk)

    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, instance=memo, user=request.user)
        if form.is_valid():
            memo = form.save()
            form.save_m2m()
            messages.success(request, 'Memo updated successfully.')
            return redirect('memos:memo_detail', pk=memo.pk)
    else:
        form = MemoForm(instance=memo, user=request.user)

    templates = MemoTemplate.objects.filter(department=request.user.department)

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

    if memo.created_by != request.user:
        messages.error(request, "You don't have permission to delete this memo.")
        return redirect('memos:memo_detail', pk=pk)

    if memo.status != 'draft':
        messages.error(request, "Only draft memos can be deleted.")
        return redirect('memos:memo_detail', pk=pk)

    memo.delete()
    messages.success(request, 'Memo deleted successfully.')
    return redirect('memos:department_dashboard')


@login_required
@require_POST
def memo_reject(request, pk):
    """Reject a memo approval request"""
    memo = get_object_or_404(Memo, pk=pk)
    approval = get_object_or_404(
        MemoApproval,
        memo=memo,
        approver=request.user,
        status='pending'
    )

    approval.status = 'rejected'
    approval.comments = request.POST.get('comments', '')
    approval.rejected_at = timezone.now()
    approval.save()

    messages.success(request, 'Memo approval rejected.')
    return redirect('memos:memo_detail', pk=pk)


@login_required
@require_POST
def memo_publish(request, pk):
    """Publish a memo"""
    memo = get_object_or_404(Memo, pk=pk)

    if memo.status != 'approved':
        messages.error(request, "Only approved memos can be published.")
        return redirect('memos:memo_detail', pk=pk)

    memo.status = 'published'
    memo.published_at = timezone.now()
    memo.save()

    messages.success(request, 'Memo published successfully.')
    return redirect('memos:memo_detail', pk=pk)

# add_reply
@login_required
def add_reply(request, pk):
    """Add a reply to a memo"""
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

# template_list

@login_required
def template_list(request):
    """List of memo templates"""
    templates = MemoTemplate.objects.filter(
        Q(department=request.user.department) | Q(department__isnull=True)
    )
    return render(request, 'memos/template_list.html', {'templates': templates})


# template_create

@login_required
def template_create(request):
    """Create a new memo template"""
    if request.method == 'POST':
        form = MemoTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.department = request.user.department
            template.save()
            form.save_m2m()
            messages.success(request, 'Template created successfully.')
            return redirect('memos:template_list')
    else:
        form = MemoTemplateForm()

    return render(request, 'memos/template_form.html', {
        'form': form,
        'action': 'Create'
    })


# template_edit

@login_required
def template_edit(request, pk):
    """Edit an existing memo template"""
    template = get_object_or_404(MemoTemplate, pk=pk)

    if request.method == 'POST':
        form = MemoTemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save()
            form.save_m2m()
            messages.success(request, 'Template updated successfully.')
            return redirect('memos:template_list')
    else:
        form = MemoTemplateForm(instance=template)

    return render(request, 'memos/template_form.html', {
        'form': form,
        'template': template,
        'action': 'Edit'
    })

# memo_status_update

@login_required
@require_POST
def memo_status_update(request, pk):
    """Update memo status"""
    memo = get_object_or_404(Memo, pk=pk)
    status = request.POST.get('status')

    if status not in [choice[0] for choice in Memo.MEMO_STATUS]:
        messages.error(request, 'Invalid status.')
        return redirect('memos:memo_detail', pk=pk)

    memo.status = status
    memo.save()

    messages.success(request, 'Memo status updated successfully.')
    return redirect('memos:memo_detail', pk=pk)


# memo_attachments

@login_required
def memo_attachments(request, pk):
    """View memo attachments"""
    memo = get_object_or_404(Memo, pk=pk)
    return render(request, 'memos/memo_attachments.html', {'memo': memo})

    
