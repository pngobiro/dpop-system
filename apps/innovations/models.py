      
# apps/innovations/models.py
from django.db import models
from django.conf import settings
from apps.statistics.models import Unit, FinancialYear, FinancialQuarter
from apps.organization.models import Department  # Assuming Department model is here

class Innovation(models.Model):
    STATUS_CHOICES = [
        ('innovation', 'Innovation'),
        ('best_practice', 'Best Practice'),
        ('rejected', 'Rejected'),
    ]

    court = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="innovations") # FK
    station = models.CharField(max_length=255)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE) # FK
    title = models.CharField(max_length=255)
    is_replication = models.BooleanField(default=False)
    source_court = models.CharField(max_length=255, blank=True, null=True)  # If replication
    category = models.CharField(max_length=100)  # Store the choice here as text
    situation_before = models.TextField()
    description = models.TextField()
    solution = models.TextField()
    replication_potential = models.TextField()
    individuals_involved = models.TextField()  # Consider ManyToManyField to User model
    stakeholders_affected = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='innovation')  # innovation, best_practice, rejected
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='submitted_innovations')
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_innovations')
    approved_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title
    
    class Meta:
              permissions = [
            ("view_all_innovations", "Can view all innovations"),  # Keep this one
            ("approve_innovation", "Can approve innovation"),
            ("reject_innovation", "Can reject innovation"),
            # Renamed permissions:
            ("can_view_innovation", "Can view innovation"),
            ("can_change_innovation", "Can change innovation"),
            ("can_delete_innovation", "Can delete innovation"),
        ]
        

class InnovationAttachment(models.Model):
    innovation = models.ForeignKey(Innovation, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='innovation_attachments/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Attachment for {self.innovation.title}"

    