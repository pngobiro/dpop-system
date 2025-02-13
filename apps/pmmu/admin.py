      
# apps/pmmu/admin.py
from django.contrib import admin
from .models import Indicator, IndicatorNote, PMMU # Updated model import
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from apps.document_management.models import Document

class DocumentInline(GenericStackedInline):
    model = Document
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 1

class IndicatorNoteInline(admin.TabularInline):
    model = IndicatorNote
    extra = 1


class IndicatorNoteAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'created_by', 'created_at')
    inlines = [DocumentInline]

admin.site.register(IndicatorNote, IndicatorNoteAdmin)


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'pmmu', 'department', 'created_at') # Updated list_display to include PMMU
    list_filter = ('pmmu__financial_year', 'department') # Updated list_filter to use pmm_financial_year
    search_fields = ('name', 'description', 'notes')
    inlines = [DocumentInline, IndicatorNoteInline]

@admin.register(PMMU) # Register PMMUAdmin
class PMMUAdmin(admin.ModelAdmin):
    list_display = ('name', 'financial_year', 'created_at')
    list_filter = ('financial_year',)
    search_fields = ('name', 'description')
    inlines = [DocumentInline] # Documents directly for PMMU

    