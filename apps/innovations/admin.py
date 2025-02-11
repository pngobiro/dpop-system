# apps/innovations/admin.py
from django.contrib import admin
from .models import Innovation, InnovationAttachment

class InnovationAttachmentInline(admin.TabularInline):  # Or StackedInline, if you prefer
    model = InnovationAttachment
    extra = 1  # Number of empty forms to show

@admin.register(Innovation)
class InnovationAdmin(admin.ModelAdmin):
    list_display = ('title', 'court', 'station', 'financial_year', 'status', 'submitted_by', 'submitted_at')
    list_filter = ('status', 'financial_year', 'court__unit_rank', 'is_replication') # Added filters
    search_fields = ('title', 'description', 'court__name', 'station')
    inlines = [InnovationAttachmentInline]
    readonly_fields = ('submitted_at', 'approved_at')  # Make timestamps read-only
    fieldsets = (
        (None, {
            'fields': (
                'court',
                'station',
                'financial_year',
                'title',
                'status', # status is also here
                'submitted_by',  # Added submitted_by
                'submitted_at',
            )
        }),
        ('Replication Information', {
            'fields': ('is_replication', 'source_court'),
            'classes': ('collapse',),  # Optional: Collapsible section
        }),
        ('Categorization', {
            'fields': ('category',),  # Added category
        }),
        ('Details', {
            'fields': (
                'situation_before',
                'description',
                'solution',
                'replication_potential',
                'individuals_involved',
                'stakeholders_affected',
            ),
        }),

        ('Approval', {  # Approval section
            'fields': ('approved_by', 'approved_at'),
             'classes': ('collapse',),
        }),

    )
    
    def save_model(self, request, obj, form, change):
      if not change:  # New object
          obj.submitted_by = request.user # auto-populate on initial save
      super().save_model(request, obj, form, change)