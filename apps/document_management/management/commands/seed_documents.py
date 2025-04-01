import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.document_management.models import Document, DocumentCategory
from apps.organization.models import Department # Needed? Maybe not directly

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample documents, including summaries and confidentiality.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding sample documents...")

        # --- Fetch prerequisites ---
        users = list(User.objects.filter(is_active=True))
        categories = list(DocumentCategory.objects.filter(is_active=True))

        if not users:
            self.stdout.write(self.style.ERROR("No active users found."))
            return
        if not categories:
            self.stdout.write(self.style.ERROR("No active document categories found. Run seed_doc_categories first."))
            return

        # --- Clear existing documents (optional) ---
        # self.stdout.write("Clearing existing documents...")
        # Document.objects.all().delete() # Use with caution

        # --- Define Realistic Document Data (Title, Summary, Category Name, Confidential Flag) ---
        document_data = [
            ("Q2 Performance Report", "Summary of key performance indicators and departmental achievements for the second quarter.", "Reports", False),
            ("Meeting Minutes - Strategy Committee", "Minutes from the strategy committee meeting held on [Date], covering agenda items X, Y, Z.", "Minutes", True), # Confidential
            ("Updated Remote Work Policy", "Revised policy outlining guidelines and procedures for remote work arrangements.", "Policies & Procedures", False),
            ("Memo: Annual Leave Scheduling", "Internal memo regarding the process for scheduling annual leave for the upcoming year.", "Memos", False),
            ("Project Alpha - Final Report", "Comprehensive final report detailing the outcomes, findings, and lessons learned from Project Alpha.", "Reports", False),
            ("Contract - Vendor XYZ", "Signed contract agreement with Vendor XYZ for software services.", "Legal & Contracts", True), # Confidential
            ("Presentation: Digital Strategy Overview", "Slide deck presenting the key pillars and roadmap of the digital transformation strategy.", "Presentations", False),
            ("Research Paper: Citizen Service Delivery Trends", "Analysis of recent trends and best practices in public sector service delivery.", "Research & Analysis", False),
            ("Leave Application Form", "Standard template for employee leave applications.", "Forms & Templates", False),
            ("Incoming Letter - Ministry of Finance", "Official correspondence received from the Ministry of Finance regarding budget allocation.", "Correspondence", True), # Confidential
            ("Q1 Audit Findings Summary", "Concise summary of internal audit findings for the first quarter.", "Reports", True), # Confidential
            ("Workshop Materials - KPI Setting", "Handouts and exercises for the workshop on setting effective Key Performance Indicators.", "Presentations", False),
        ]

        # --- Create Documents ---
        created_count = 0
        for title, summary, cat_name, is_confidential in document_data:
            category = next((c for c in categories if c.name == cat_name), None)
            if not category:
                self.stdout.write(self.style.WARNING(f"Category '{cat_name}' not found, skipping document: {title}"))
                continue

            # Create document (not linked to project/task initially)
            Document.objects.create(
                title=title,
                description=summary, # Use summary here
                category=category,
                file=None, # No actual file
                file_type=random.choice(['pdf', 'docx', 'xlsx']),
                file_size=random.randint(50000, 2000000),
                storage_type='local',
                uploaded_by=random.choice(users),
                is_confidential=is_confidential,
                status='approved', # Assume seeded docs are approved
                source_module='document_management' # Default source
                # content_type, object_id, source_object left null initially
            )
            created_count += 1
            self.stdout.write(f"  Created document: {title} (Confidential: {is_confidential})")

        self.stdout.write(self.style.SUCCESS(f"Document seeding complete. {created_count} documents created."))