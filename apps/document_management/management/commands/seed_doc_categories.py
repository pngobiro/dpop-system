from django.core.management.base import BaseCommand
from apps.document_management.models import DocumentCategory

class Command(BaseCommand):
    help = 'Seeds the database with essential document categories.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding document categories...")

        categories = [
            ("Minutes", "Meeting minutes and records of decisions."),
            ("Reports", "Periodic and ad-hoc reports (e.g., performance, financial, audit)."),
            ("Memos", "Internal memorandums and communications."),
            ("Policies & Procedures", "Official organizational policies and standard operating procedures."),
            ("Forms & Templates", "Standardized forms and document templates."),
            ("Presentations", "Slide decks and presentation materials."),
            ("Research & Analysis", "Research papers, data analysis, and findings."),
            ("Legal & Contracts", "Legal documents, contracts, and agreements."),
            ("Correspondence", "Official incoming and outgoing letters."),
            ("Other", "Miscellaneous documents not fitting other categories."),
        ]

        created_count = 0
        for name, description in categories:
            category, created = DocumentCategory.objects.get_or_create(
                name=name,
                defaults={'description': description, 'is_active': True}
            )
            if created:
                self.stdout.write(f"  Created category: {name}")
                created_count += 1
            else:
                self.stdout.write(f"  Category already exists: {name}")

        self.stdout.write(self.style.SUCCESS(f"Document category seeding complete. {created_count} new categories created."))