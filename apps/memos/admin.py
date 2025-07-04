from django.contrib import admin
from .models import (
    MemoType, MemoCategory, PriorityLevel, MemoStatus, MemoWorkflow, WorkflowStep,
    Memo, ActionItem, Delegation, MemoDocument, MemoTimeline, CommentThread, ThreadComment
)


@admin.register(MemoType)
class MemoTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'requires_approval']
    list_filter = ['is_active', 'requires_approval']
    search_fields = ['name', 'code']


@admin.register(MemoCategory)
class MemoCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(PriorityLevel)
class PriorityLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'response_time_days']
    ordering = ['level']


@admin.register(MemoStatus)
class MemoStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_final', 'is_active', 'order']
    list_filter = ['is_final', 'is_active']
    ordering = ['order']


@admin.register(MemoWorkflow)
class MemoWorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'is_default', 'is_active']
    list_filter = ['department', 'is_default', 'is_active']
    search_fields = ['name']


@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'step_order', 'name', 'role_required', 'is_optional']
    list_filter = ['workflow', 'is_optional']
    ordering = ['workflow', 'step_order']


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'title', 'memo_type', 'status', 'department', 'created_by', 'created_at']
    list_filter = ['memo_type', 'status', 'department', 'is_physical', 'is_confidential', 'priority']
    search_fields = ['reference_number', 'title', 'subject']
    readonly_fields = ['id', 'reference_number', 'created_at', 'updated_at']
    raw_id_fields = ['created_by', 'sender_internal']
    filter_horizontal = ['recipient_departments', 'recipient_users']
    date_hierarchy = 'created_at'


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'memo', 'assigned_to', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'assigned_to']
    search_fields = ['title', 'memo__reference_number']
    raw_id_fields = ['memo', 'assigned_to', 'assigned_by']


@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ['memo', 'from_user', 'to_user', 'status', 'delegated_at']
    list_filter = ['status']
    raw_id_fields = ['memo', 'from_user', 'to_user']


@admin.register(MemoTimeline)
class MemoTimelineAdmin(admin.ModelAdmin):
    list_display = ['memo', 'event_type', 'user', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['memo__reference_number', 'description']
    raw_id_fields = ['memo', 'user']
    readonly_fields = ['timestamp']


@admin.register(CommentThread)
class CommentThreadAdmin(admin.ModelAdmin):
    list_display = ['memo', 'title', 'created_by', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    raw_id_fields = ['memo', 'created_by']


@admin.register(ThreadComment)
class ThreadCommentAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at', 'is_edited']
    list_filter = ['is_edited', 'created_at']
    raw_id_fields = ['thread', 'author']
    readonly_fields = ['created_at', 'updated_at']
