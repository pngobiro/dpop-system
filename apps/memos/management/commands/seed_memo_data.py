"""
Seed data for the new memo system
Run this after migrations to populate initial data
"""

from django.core.management.base import BaseCommand
from apps.memos.models import (
    MemoType, MemoCategory, PriorityLevel, MemoStatus
)


class Command(BaseCommand):
    help = 'Create initial data for the memo system'

    def handle(self, *args, **options):
        # Create Memo Types
        memo_types_data = [
            {'name': 'Internal Memo', 'code': 'INT', 'description': 'Internal communication within the organization'},
            {'name': 'External Letter', 'code': 'EXT', 'description': 'Communication with external organizations'},
            {'name': 'Circular', 'code': 'CIR', 'description': 'General announcements and policies'},
            {'name': 'Directive', 'code': 'DIR', 'description': 'Official directives and instructions'},
        ]
        
        for type_data in memo_types_data:
            memo_type, created = MemoType.objects.get_or_create(
                name=type_data['name'],
                defaults=type_data
            )
            if created:
                self.stdout.write(f"Created memo type: {memo_type.name}")

        # Create Categories
        categories_data = [
            {'name': 'Administrative', 'color': '#007bff', 'icon': 'fas fa-cogs'},
            {'name': 'Financial', 'color': '#28a745', 'icon': 'fas fa-dollar-sign'},
            {'name': 'Human Resources', 'color': '#ffc107', 'icon': 'fas fa-users'},
            {'name': 'Legal', 'color': '#dc3545', 'icon': 'fas fa-gavel'},
            {'name': 'Operations', 'color': '#6f42c1', 'icon': 'fas fa-cog'},
            {'name': 'General', 'color': '#6c757d', 'icon': 'fas fa-file-alt'},
        ]
        
        for cat_data in categories_data:
            category, created = MemoCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create Priority Levels
        priorities_data = [
            {'name': 'Urgent', 'level': 1, 'color': '#dc3545', 'response_time_days': 1},
            {'name': 'High', 'level': 2, 'color': '#fd7e14', 'response_time_days': 3},
            {'name': 'Medium', 'level': 3, 'color': '#ffc107', 'response_time_days': 7},
            {'name': 'Low', 'level': 4, 'color': '#28a745', 'response_time_days': 14},
            {'name': 'Information', 'level': 5, 'color': '#6c757d', 'response_time_days': None},
        ]
        
        for priority_data in priorities_data:
            priority, created = PriorityLevel.objects.get_or_create(
                name=priority_data['name'],
                defaults=priority_data
            )
            if created:
                self.stdout.write(f"Created priority: {priority.name}")

        # Create Status Options
        statuses_data = [
            {'name': 'Draft', 'color': '#6c757d', 'order': 1},
            {'name': 'Pending Review', 'color': '#ffc107', 'order': 2},
            {'name': 'Under Review', 'color': '#fd7e14', 'order': 3},
            {'name': 'Approved', 'color': '#28a745', 'order': 4},
            {'name': 'Rejected', 'color': '#dc3545', 'order': 5, 'is_final': True},
            {'name': 'Dispatched', 'color': '#007bff', 'order': 6},
            {'name': 'Received', 'color': '#20c997', 'order': 7},
            {'name': 'Completed', 'color': '#198754', 'order': 8, 'is_final': True},
            {'name': 'Archived', 'color': '#495057', 'order': 9, 'is_final': True},
        ]
        
        for status_data in statuses_data:
            status, created = MemoStatus.objects.get_or_create(
                name=status_data['name'],
                defaults=status_data
            )
            if created:
                self.stdout.write(f"Created status: {status.name}")

        self.stdout.write(
            self.style.SUCCESS('Successfully created initial memo system data')
        )
