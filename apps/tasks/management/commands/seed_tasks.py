import random
import os
import datetime # Import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone # Import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from apps.organization.models import Department
from apps.tasks.models import Project, Task, Comment
from apps.document_management.models import Document # Import Document model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with realistic sample task projects, tasks, comments, and fake attachments for each department.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding database with realistic data for each department...")

        # --- Fetch existing data ---
        departments = list(Department.objects.filter(is_active=True))
        users = list(User.objects.filter(is_active=True))

        if not departments:
            self.stdout.write(self.style.ERROR("No active departments found. Please seed departments first."))
            return
        if not users:
            self.stdout.write(self.style.ERROR("No active users found. Please seed users first."))
            return

        # --- Clear existing task data ---
        self.stdout.write("Clearing existing task & related document data...")
        try:
            project_ct = ContentType.objects.get_for_model(Project)
            task_ct = ContentType.objects.get_for_model(Task)
            Document.objects.filter(content_type__in=[project_ct, task_ct]).delete()
        except ContentType.DoesNotExist:
             self.stdout.write(self.style.WARNING("ContentType for Project or Task not found. Skipping document clearing."))
        Comment.objects.all().delete()
        Task.objects.all().delete()
        Project.objects.all().delete()

        # --- Define Realistic Data Lists ---
        # (Keep the same lists as before)
        project_data = [
            ("Performance Framework Review FY24/25", "Review and update the organizational performance metrics and reporting framework for the current fiscal year."),
            ("Digital Transformation Strategy Roadmap", "Develop a detailed 3-year roadmap for digitalizing core citizen services."),
            ("Stakeholder Engagement Plan Q3-Q4", "Create a comprehensive plan for engaging key internal and external stakeholders for the second half of the year."),
            ("Operational Risk Assessment Update", "Conduct the bi-annual update of the operational risk register and mitigation plans."),
            ("Annual Work Plan Consolidation FY25/26", "Coordinate the development, review, and consolidation of the annual work plan for the upcoming fiscal year."),
            ("Policy Brief: New Data Privacy Regulations", "Compile recent data privacy regulations into accessible briefs for management and relevant departments."),
            ("Performance Data Dashboard Phase 1", "Implement Phase 1 of the platform for centralizing and visualizing key performance indicators."),
            ("Strategic Planning Workshop Series", "Design and facilitate a series of workshops on strategic planning methodologies for department heads."),
            ("Service Charter Public Consultation", "Coordinate and analyze feedback from the public consultation on the revised service charter."),
            ("Inter-Departmental KPI Alignment Initiative", "Facilitate initiative to ensure alignment of Key Performance Indicators across related departments.")
        ]

        task_data = [
            ("Review existing performance metrics", "Analyze the relevance and effectiveness of current KPIs."),
            ("Draft updated KPI definitions", "Propose revised definitions and calculation methods for key metrics."),
            ("Schedule framework review meeting with Directors", "Coordinate schedules and prepare agenda for the review meeting."),
            ("Develop roadmap presentation slides", "Create a compelling presentation outlining the digital transformation roadmap."),
            ("Identify key stakeholder groups", "Map internal and external stakeholders relevant to Q3/Q4 objectives."),
            ("Draft communication plan for stakeholders", "Outline key messages, channels, and timelines for stakeholder engagement."),
            ("Review departmental risk submissions", "Analyze risk registers submitted by various departments."),
            ("Update central operational risk register", "Consolidate findings and update the main risk register."),
            ("Collect departmental work plan drafts", "Gather initial work plan submissions from all departments."),
            ("Consolidate work plan budget requests", "Aggregate budget requirements outlined in departmental plans."),
            ("Summarize key points of new regulations", "Extract the most critical aspects of the data privacy laws."),
            ("Draft internal communication memo on privacy", "Prepare a memo for staff regarding the implications of the new regulations."),
            ("Define dashboard data source requirements", "Specify the data needed and its format for the performance dashboard."),
            ("Evaluate potential dashboard vendor solutions", "Research and compare suitable business intelligence tools."),
            ("Develop workshop module 1: SWOT Analysis", "Create training materials and exercises for the SWOT analysis module."),
            ("Identify target audience for planning workshops", "Determine which managers and staff should attend the workshops."),
            ("Compile public feedback on service charter", "Gather and categorize comments received during the consultation period."),
            ("Draft revised service charter sections", "Update specific sections based on analyzed public feedback."),
            ("Map KPI dependencies between departments", "Identify how KPIs in one department impact others."),
            ("Facilitate KPI alignment meeting (Dept A & B)", "Lead a meeting to resolve conflicting or misaligned KPIs between two key departments.")
        ]

        comment_snippets = [
            "Draft sent for review.", "Meeting scheduled for next Tuesday.", "Can we get the latest figures for this?",
            "Approved. Proceed to next step.", "Need clarification on point 3.", "This looks good, thanks!",
            "Budget allocation confirmed.", "Waiting for feedback from Legal.", "Updated timeline attached.",
            "Let's discuss this further in our next sync.", "Risk identified, mitigation plan needed.",
            "Data source confirmed.", "Presentation ready.", "Stakeholder list finalized.", "Minor revisions needed."
        ]

        attachment_titles = [
            "Draft Report", "Meeting Minutes", "Budget Proposal", "Project Plan", "Requirements Doc",
            "Presentation Slides", "Feedback Summary", "Risk Register Extract", "Policy Document",
            "Analysis Results", "Communication Plan", "User Guide", "Technical Specs"
        ]

        all_created_projects = []
        all_created_tasks = []

        # --- Iterate through Departments ---
        project_data_index = 0 # Keep track of project ideas used
        for dept in departments:
            self.stdout.write(f"--- Seeding for Department: {dept.name} ---")
            num_projects_for_dept = 10 # Create a fixed number of projects per dept
            dept_projects = []

            for i in range(num_projects_for_dept):
                # Cycle through project data if needed, make names unique per run
                proj_name_base, proj_desc = project_data[project_data_index % len(project_data)]
                project_name = f"{dept.name[:15]} - {proj_name_base} (Set {project_data_index // len(project_data) + 1}, Proj {i+1})"
                project_data_index += 1

                owner = random.choice(users)
                project = Project.objects.create(
                    name=project_name,
                    description=proj_desc,
                    owner=owner,
                    department=dept
                )
                dept_projects.append(project)
                all_created_projects.append(project)
                self.stdout.write(f"  Created Project: {project.name}")

            if not dept_projects:
                self.stdout.write(self.style.WARNING(f"  No projects created for {dept.name}, skipping tasks."))
                continue

            # --- Create Tasks for this Department's Projects ---
            dept_tasks = []
            target_tasks_per_dept = 110 # Aim for slightly more than 100
            task_data_index = 0

            for i in range(target_tasks_per_dept):
                project = random.choice(dept_projects) # Assign task to a random project in this dept
                task_title_base, task_desc_base = task_data[task_data_index % len(task_data)]
                task_title = f"{task_title_base} (DeptTask {i+1})" # Make titles slightly unique per dept
                task_data_index += 1

                creator = random.choice(users)
                assignee = random.choice(users) if random.random() > 0.1 else None
                priority = random.choice(Task.PriorityChoices.values)

                # Explicitly control status and due date for variety
                rand_status_choice = random.random()
                if rand_status_choice < 0.25: # ~25% DONE
                    status = Task.StatusChoices.DONE
                    due_date = timezone.now().date() - datetime.timedelta(days=random.randint(5, 60)) # Done tasks usually have past due dates
                elif rand_status_choice < 0.50: # ~25% Overdue
                    status = random.choice([Task.StatusChoices.TODO, Task.StatusChoices.IN_PROGRESS, Task.StatusChoices.BLOCKED])
                    due_date = timezone.now().date() - datetime.timedelta(days=random.randint(1, 15)) # Past due date, not DONE
                elif rand_status_choice < 0.90: # ~40% In Progress/Todo
                    status = random.choice([Task.StatusChoices.TODO, Task.StatusChoices.IN_PROGRESS])
                    due_date = random.choice([None] + [timezone.now().date() + datetime.timedelta(days=random.randint(0, 90)) for _ in range(3)]) # Future or no due date
                else: # ~10% Blocked
                    status = Task.StatusChoices.BLOCKED
                    due_date = random.choice([None] + [timezone.now().date() + datetime.timedelta(days=random.randint(-10, 90)) for _ in range(3)])
                # Generate start_date (usually before due_date if due_date exists) - Correctly indented
                start_date = None
                if due_date:
                    # Start date between 1 and 30 days before due date, or today if due date is soon
                    days_before = random.randint(1, 30)
                    potential_start = due_date - datetime.timedelta(days=days_before)
                    # Ensure start date isn't accidentally *after* due date for short tasks
                    start_date = min(potential_start, due_date - datetime.timedelta(days=1))
                    # Don't start too far in past relative to today either
                    start_date = max(start_date, timezone.now().date() - datetime.timedelta(days=random.randint(0, 45)))
                elif random.random() < 0.5: # 50% chance of start date even if no due date
                    start_date = timezone.now().date() - datetime.timedelta(days=random.randint(0, 15))

                # Create Task - Correctly indented
                task = Task.objects.create(
                    project=project, title=task_title, description=task_desc_base,
                    status=status, priority=priority, assignee=assignee,
                    creator=creator, start_date=start_date, due_date=due_date # Added start_date
                )
                # Removed extra parenthesis from previous line
                dept_tasks.append(task)
                all_created_tasks.append(task)

            self.stdout.write(f"  Created {len(dept_tasks)} tasks for this department.")

        # --- Create Comments (for all created tasks) ---
        self.stdout.write("Creating sample comments...")
        comment_count = 0
        for task in all_created_tasks:
            if random.random() > 0.3:
                num_comments = random.randint(1, 6)
                for _ in range(num_comments):
                    author = random.choice(users)
                    comment = Comment.objects.create(
                        task=task, author=author, content=random.choice(comment_snippets)
                    )
                    comment_count += 1
        self.stdout.write(f"  Added {comment_count} comments overall.")

        # --- Create Fake Attachments (for all created projects/tasks) ---
        self.stdout.write("Creating fake attachments...")
        attachment_count = 0
        try:
            project_content_type = ContentType.objects.get_for_model(Project)
            task_content_type = ContentType.objects.get_for_model(Task)

            for project in all_created_projects:
                if random.random() < 0.4:
                    num_attachments = random.randint(1, 3)
                    for i in range(num_attachments):
                        doc_title = f"{project.name[:20]}... - {random.choice(attachment_titles)}"
                        Document.objects.create(
                            title=doc_title, description=f"Supporting document for project: {project.name}",
                            file=None, file_type=random.choice(['pdf', 'docx', 'xlsx']),
                            file_size=random.randint(50000, 5000000), storage_type='local',
                            uploaded_by=random.choice(users), content_type=project_content_type,
                            object_id=project.id, source_module='tasks'
                        )
                        attachment_count += 1

            for task in all_created_tasks:
                 if random.random() < 0.25:
                    num_attachments = random.randint(1, 2)
                    for i in range(num_attachments):
                        doc_title = f"{task.title[:20]}... - {random.choice(attachment_titles)}"
                        Document.objects.create(
                            title=doc_title, description=f"Reference material for task: {task.title}",
                            file=None, file_type=random.choice(['pdf', 'png', 'txt']),
                            file_size=random.randint(10000, 1000000), storage_type='local',
                            uploaded_by=random.choice(users), content_type=task_content_type,
                            object_id=task.id, source_module='tasks'
                        )
                        attachment_count += 1

            self.stdout.write(f"  Added {attachment_count} fake attachments overall.")

        except ContentType.DoesNotExist:
             self.stdout.write(self.style.ERROR("ContentType for Project or Task not found. Cannot create attachments."))
        except ImportError:
             self.stdout.write(self.style.ERROR("Document model not found. Cannot create attachments."))
        except Exception as e:
             self.stdout.write(self.style.ERROR(f"An error occurred creating attachments: {e}"))

        self.stdout.write(self.style.SUCCESS("Database seeding with realistic data completed successfully!"))