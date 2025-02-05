# apps/meetings/admin.py
from django.contrib import admin
from .models import Meeting, MeetingParticipant, MeetingDocument

class MeetingParticipantInline(admin.TabularInline):
    model = MeetingParticipant
    extra = 1

class MeetingDocumentInline(admin.TabularInline):
    model = MeetingDocument
    extra = 1

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'date', 'meeting_type', 'meeting_mode', 'status')
    list_filter = ('department', 'meeting_type', 'meeting_mode', 'status', 'date')
    search_fields = ('title', 'agenda', 'department__name')
    date_hierarchy = 'date'
    inlines = [MeetingParticipantInline, MeetingDocumentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'meeting_type', 'meeting_mode', 'status')
        }),
        ('Timing', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Location', {
            'fields': ('physical_location',)
        }),
        ('Virtual Meeting Details', {
            'fields': ('virtual_platform', 'virtual_meeting_url', 'virtual_meeting_id', 'virtual_meeting_password'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('agenda', 'minutes')
        }),
        ('Recording', {
            'fields': ('recording_url', 'has_recording'),
            'classes': ('collapse',)
        }),
    )