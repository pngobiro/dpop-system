# apps/mail/management/commands/seed_mail.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.mail.models import PhysicalMail, MailActivity, MailAssignment, MailMovement
from apps.organization.models import Department
from faker import Faker
import random
from datetime import timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds sample mail data (PhysicalMail, MailActivity, MailAssignment, MailMovement)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding mail data...')

        # --- Prerequisites ---
        departments = Department.objects.all()
        if not departments.exists():
            self.stdout.write(self.style.ERROR('No departments found. Run seed_organization first.'))
            return

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Run seed_organization first.'))
            return

        # --- Sample Data ---
        mail_subjects = [
            'Request for Budget Approval', 'Monthly Performance Report',
            'Meeting Minutes: Department Heads', 'Policy Update Notification',
            'Training Program Schedule', 'Equipment Purchase Request',
            'Staff Transfer Notice', 'IT System Maintenance',
            'Quarterly Review Summary', 'Holiday Schedule Update',
            'Complaint from Citizen', 'Court Order', 'Summons', 'Legal Opinion Request',
            'Invitation to Tender', 'Contract Agreement', 'Internal Audit Report' # Added more
        ]
        mail_types = ['incoming', 'outgoing']
        statuses = ['received', 'in_transit', 'delivered', 'pending_dispatch', 'dispatched', 'acknowledged', 'archived']
        priorities = ['normal', 'express', 'urgent']
        delivery_methods = ['hand_delivery', 'postal', 'courier', 'diplomatic_bag']

        # --- Create Mail ---
        for _ in range(50):  # Create 50 mail entries
            department = random.choice(departments)
            creator = random.choice(users.filter(departments=department)) # More robust user selection.
            mail_type = random.choice(mail_types)
            status = random.choice(statuses)
            priority = random.choice(priorities)
            delivery_method = random.choice(delivery_methods)

            # Generate dates
            base_date = timezone.now() - timedelta(days=random.randint(0, 90))
            received_date = base_date if mail_type == 'incoming' else None
            sent_date = base_date if mail_type == 'outgoing' else None

            mail = PhysicalMail.objects.create(
                # tracking_number=generate_tracking_number(),   # Handled by pre_save signal
                mail_type=mail_type,
                subject=random.choice(mail_subjects),
                description=fake.paragraph(nb_sentences=3),
                date_received=received_date,
                date_sent=sent_date,
                department=department,
                priority=priority,
                confidential=random.choice([True, False]),
                file_number=f"FILE/{random.randint(1000, 9999)}/{base_date.year}",
                delivery_method=delivery_method,
                weight=random.uniform(50, 2000) if delivery_method != 'hand_delivery' else None,  # Weight in grams
                postage_cost=random.uniform(10, 500) if delivery_method == 'postal' else None,
                courier_name=fake.company() if delivery_method == 'courier' else "",
                courier_tracking_number=fake.uuid4() if delivery_method == 'courier' else "",
                status=status,
                created_by=creator,
                created_at=base_date,
                updated_at=base_date,
                sender_name=fake.name(),
                sender_address=fake.address(),
                sender_phone=fake.phone_number(),
                recipient_name=fake.name(),
                recipient_address=fake.address(),
                recipient_phone=fake.phone_number(),
                requires_response=random.choice([True, False]),
                response_deadline=base_date + timedelta(days=random.randint(7, 30)) if random.choice([True, False]) else None,
            )
            # --- Create Assignments (for some mail) ---
            if random.choice([True, False]):
                assigned_to = random.choice(users.filter(departments=department)) # Assign to users *within* the department
                due_date = base_date + timedelta(days=random.randint(7,30))
                completed = random.choice([True, False])
                MailAssignment.objects.create(
                    mail=mail,
                    assigned_to=assigned_to,
                    assigned_by=creator,
                    assigned_at=base_date + timedelta(days=1),
                    due_date=due_date,
                    completed=completed,
                    completed_at=due_date if completed else None,
                    notes=fake.sentence(),
                    current_location = department.name,
                    acknowledgment_required=random.choice([True, False])
                )

             # --- Create Movements (for some mail) ---
            if random.choice([True, False]):
                from_location = random.choice(departments).name  # Random from location
                to_location = random.choice(departments).name    # Random to location
                handler = random.choice(users)               # Random handler (could be anyone)

                MailMovement.objects.create(
                    mail=mail,
                    from_location=from_location,
                    to_location=to_location,
                    handler=handler,
                    timestamp=timezone.now(),  # Use current time for movement
                    notes=fake.sentence(),
                    received_by=handler if random.choice([True, False]) else "",  # Optional received by
                    received_at=timezone.now() if random.choice([True, False]) else None,  # Optional receive time
                )


            # --- Create Response Mail (for some items that require a response) ---
            if mail.requires_response and random.choice([True, False]):
              response_date = base_date + timedelta(days=random.randint(1,14))

              response = PhysicalMail.objects.create(
                  mail_type = 'outgoing' if mail.mail_type == 'incoming' else 'incoming',
                  subject=f"Re: {mail.subject}",
                  description=fake.paragraph(nb_sentences=3),
                  date_sent= response_date,
                  department=department,
                  priority=mail.priority,
                  confidential=mail.confidential,
                  file_number=mail.file_number,
                  status='dispatched',
                  created_by=creator,
                  created_at=base_date,
                  updated_at=base_date,
                  sender_name=mail.recipient_name,
                  sender_address=mail.recipient_address,
                  sender_phone= mail.recipient_phone,
                  recipient_name=mail.sender_name,
                  recipient_address=mail.sender_address,
                  recipient_phone=mail.sender_phone,
                  requires_response=False,
                  response_deadline=None,

              )
              mail.response_mail = response
              mail.save()



        self.stdout.write(self.style.SUCCESS('Successfully seeded mail data'))