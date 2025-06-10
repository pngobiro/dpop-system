from django.db import models

# Create your models here.

from django.db import models

class UnitRank(models.Model):
    name = models.CharField(max_length=255)
    is_court = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class FinancialYear(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return self.name

class FinancialQuarter(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    financial_year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE)
    quarter_number = models.IntegerField(
        help_text='The financial quarter in which the month falls. It is either 1, 2, 3, or 4'
    )

    def get_quarter_name(self):
        """Format quarter name with dates in dd/mm/yyyy format"""
        if isinstance(self.start_date, str):
            return f"{self.name} ({self.start_date} - {self.end_date})"
        
        return "{} ({} - {})".format(
            self.name,
            self.start_date.strftime('%d/%m/%Y') if self.start_date else 'N/A',
            self.end_date.strftime('%d/%m/%Y') if self.end_date else 'N/A'
        )

    def __str__(self):
        return self.get_quarter_name()
    
class Unit(models.Model):
    name = models.CharField(max_length=255)
    dcrt_unique_id = models.CharField(max_length=255, blank=True, null=True)
    unique_id = models.CharField(max_length=255)
    unique_code = models.CharField(max_length=255)
    unit_rank = models.ForeignKey(UnitRank, on_delete=models.CASCADE)
    head_id_fk = models.IntegerField()
    subhead_id_fk = models.IntegerField()
    has_division = models.BooleanField(default=False)
    is_court = models.BooleanField(default=False)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    is_template = models.BooleanField(default=False)
    template_unit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='template_for')
    
    def __str__(self):
        return self.name

class Months(models.Model):
    name = models.CharField(max_length=255)
    month_number = models.IntegerField(help_text='The calendar month number (1-12)')
    financial_quarter = models.IntegerField(help_text='The financial quarter in which the month falls. It is either 1, 2, 3, or 4')

    def __str__(self):
        return self.name
    
class Division(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=50)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class CaseOutcome(models.Model):
    """Case outcomes specific to each UnitRank (e.g., for ELRC)"""
    name = models.CharField(max_length=255)  # e.g., "Adjournment", "Case Registered/Filed"
    description = models.TextField(null=True, blank=True)
    unit_rank = models.ForeignKey(UnitRank, on_delete=models.CASCADE, related_name='case_outcomes')

    class Meta:
        verbose_name_plural = "Case Outcomes"
        unique_together = [('name', 'unit_rank')]  # Each outcome should be unique within a rank
        ordering = ['unit_rank', 'name']

    def __str__(self):
        return f"{self.name} ({self.unit_rank.name})"

class CaseCategory(models.Model):
    """Case categories specific to each UnitRank (e.g., ELRCA for ELRC Appeals)"""
    name = models.CharField(max_length=255)  # e.g., "Appeals", "Claims/Causes"
    code = models.CharField(max_length=10)   # e.g., "ELRCA", "ELRCC"
    unit_rank = models.ForeignKey(UnitRank, on_delete=models.CASCADE, related_name='case_categories')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Case Categories"
        unique_together = [
            ('code', 'unit_rank'),  # Each code should be unique within a rank
            ('name', 'unit_rank')   # Each name should be unique within a rank
        ]
        ordering = ['unit_rank', 'code']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.unit_rank.name})"

    @property
    def full_code(self):
        """Returns the full case code pattern (e.g., 'ELRCA' for ELRC Appeals)"""
        return self.code

class AdjournmentReason(models.Model):
    """Adjournment reasons specific to each UnitRank."""
    name = models.CharField(max_length=255)  # e.g., "Advocate not present", "Court on its own motion"
    unit_rank = models.ForeignKey(UnitRank, on_delete=models.CASCADE, related_name='adjournment_reasons')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Adjournment Reasons"
        unique_together = [('name', 'unit_rank')]  # Each reason should be unique within a rank
        ordering = ['unit_rank', 'name']

    def __str__(self):
        return f"{self.name} ({self.unit_rank.name})"

class CaseActivityType(models.Model):
    """Types of activities/proceedings a case can be scheduled for, specific to a UnitRank."""
    name = models.CharField(max_length=255, unique=True) # Ensure names are unique
    unit_rank = models.ForeignKey(UnitRank, on_delete=models.CASCADE, related_name='activity_types')
    description = models.TextField(blank=True, null=True) # Optional description

    class Meta:
        unique_together = ('name', 'unit_rank') # Ensure unique name per rank
        ordering = ['unit_rank', 'name']

    def __str__(self):
        return f"{self.name} ({self.unit_rank.name})"
    
# Add CaseCategory to case_number_code choices
# Example: When case_number_code is "ELRCA", it refers to an ELRC Appeal case
class DcrtData(models.Model):
    # no constraints on foreign keys

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    financial_quarter = models.ForeignKey(FinancialQuarter, on_delete=models.CASCADE)
    month = models.ForeignKey(Months, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    today_date_day = models.IntegerField(null=True, blank=True)
    today_date_month = models.CharField(max_length=255, null=True, blank=True)
    today_date_year = models.CharField(max_length=255, null=True, blank=True)
    name_of_court = models.CharField(max_length=255, null=True, blank=True)
    case_number_code = models.ForeignKey(CaseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='dcrt_entries')
    case_number_number = models.IntegerField(null=True, blank=True)
    case_number_day = models.IntegerField(null=True, blank=True)
    case_number_month = models.CharField(max_length=255, null=True, blank=True)
    case_number_year = models.IntegerField(null=True, blank=True)
    appeal_number_court_name = models.CharField(max_length=255, null=True, blank=True)
    appeal_number_code = models.CharField(max_length=255, null=True, blank=True)
    appeal_number_number = models.IntegerField(null=True, blank=True)
    appeal_number_year = models.IntegerField(null=True, blank=True)
    specific_case_type = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_1 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_2 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_3 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_4 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_5 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_6 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_7 = models.CharField(max_length=255, null=True, blank=True)
    judicial_officer_8 = models.CharField(max_length=255, null=True, blank=True)
    case_coming_for = models.CharField(max_length=255, null=True, blank=True)
    case_outcome = models.CharField(max_length=255, null=True, blank=True)
    adjournment_reason = models.CharField(max_length=255, null=True, blank=True)
    date_of_next_activity_day = models.IntegerField(null=True, blank=True)
    date_of_next_activity_month = models.CharField(max_length=255, null=True, blank=True)
    date_of_next_activity_year = models.IntegerField(null=True, blank=True)
    no_of_plaintiffs_or_appellants_male = models.IntegerField(null=True, blank=True)
    no_of_plaintiffs_or_appellants_female = models.IntegerField(null=True, blank=True)
    no_of_plaintiffs_or_appellants_organization = models.IntegerField(null=True, blank=True)
    no_of_defendants_accused_male = models.IntegerField(null=True, blank=True)
    no_of_defendants_accused_female = models.IntegerField(null=True, blank=True)
    no_of_defendants_accused_organization = models.IntegerField(null=True, blank=True)
    parties_have_legal_representation = models.CharField(max_length=255,null=True, blank=True)
    no_of_witnesses_in_court_d = models.IntegerField(null=True, blank=True)
    no_of_witnesses_in_court_w = models.IntegerField(null=True, blank=True)
    no_of_accused_remanded = models.IntegerField(null=True, blank=True)
    last_date_of_submission_of_case_file_day = models.CharField(max_length=255, null=True, blank=True)
    last_date_of_submission_of_case_file_month = models.CharField(max_length=255, null=True, blank=True)
    last_date_of_submission_of_case_file_year = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    
class UnitDivision(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
