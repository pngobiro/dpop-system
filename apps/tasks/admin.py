from django.contrib import admin
from .models import Project, Task, Comment
from django.contrib.contenttypes.admin import GenericTabularInline

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

# Inline for Comments on Task admin page
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1 # Number of empty forms to display
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)

# Inline for Attachments (Documents) - Reusable for Task and Project
if Document:
    class DocumentInline(GenericTabularInline):
        model = Document
        extra = 1
        fields = ('title', 'file', 'storage_type', 'drive_file_id', 'uploaded_by', 'created_at')
        readonly_fields = ('uploaded_by', 'created_at', 'file_type', 'file_size')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display_fields = ['name', 'owner', 'created_at', 'updated_at']
    list_filter_fields = ['owner', 'created_at']
    inlines_list = [] # Start with empty list for inlines

    if Department:
        list_display_fields.insert(1, 'department')
        list_filter_fields.insert(0, 'department')

    if Document:
        inlines_list.append(DocumentInline) # Add document inline if available

    list_display = tuple(list_display_fields)
    search_fields = ('name', 'description', 'department__name' if Department else 'name')
    list_filter = tuple(list_filter_fields)
    readonly_fields = ('created_at', 'updated_at')
    fields = ('name', 'description', 'owner', 'department' if Department else None, 'created_at', 'updated_at')
    fields = tuple(filter(None, fields))
    inlines = inlines_list # Assign the constructed inlines list


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assignee', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'project__name')
    list_filter = ('status', 'priority', 'project', 'assignee', 'due_date', 'project__department' if Department else 'project')
    readonly_fields = ('created_at', 'updated_at', 'creator')
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'description')
        }),
        ('Details', {
            'fields': ('status', 'priority', 'assignee', 'due_date')
        }),
        ('Metadata', {
            'fields': ('creator', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    # Add inlines based on whether Document model is available
    inlines = [CommentInline]
    if Document:
        inlines.append(DocumentInline) # DocumentInline defined above

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'task', 'created_at', 'content_preview')
    search_fields = ('content', 'author__username', 'task__title')
    list_filter = ('created_at', 'author')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
