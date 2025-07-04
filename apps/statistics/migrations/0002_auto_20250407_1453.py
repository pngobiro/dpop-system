# Generated by Django 3.2.25 on 2025-04-07 14:53

from django.db import migrations, models
import django.db.models.deletion
from django.db import migrations, models

# --- Data Migration Function ---
def seed_case_activity_types(apps, schema_editor):
    """
    Populates CaseActivityType based on distinct values in DcrtData.case_coming_for (CharField).
    Associates them with the correct UnitRank based on the DcrtData record's Unit.
    """
    DcrtData = apps.get_model('statistics', 'DcrtData')
    CaseActivityType = apps.get_model('statistics', 'CaseActivityType')
    UnitRank = apps.get_model('statistics', 'UnitRank')
    db_alias = schema_editor.connection.alias

    distinct_values = DcrtData.objects.using(db_alias).values_list(
        'case_coming_for', 'unit__unit_rank_id'
    ).distinct()

    created_count = 0
    skipped_count = 0
    
    print("\nSeeding CaseActivityType table...")
    for name, rank_id in distinct_values:
        if name and rank_id:
            try:
                unit_rank = UnitRank.objects.using(db_alias).get(id=rank_id)
                # Use update_or_create to handle potential duplicates gracefully if run multiple times
                obj, created = CaseActivityType.objects.using(db_alias).update_or_create(
                    name=name,
                    unit_rank=unit_rank,
                    defaults={'description': name} # Optional: set description
                )
                if created:
                    created_count += 1
            except UnitRank.DoesNotExist:
                 print(f"  Warning: UnitRank with ID {rank_id} not found for activity '{name}'. Skipping.")
                 skipped_count += 1
            except Exception as e:
                 print(f"  Error creating/updating activity '{name}' for Rank ID {rank_id}: {e}")
                 skipped_count += 1
        else:
            if name:
                 print(f"  Warning: Skipping activity '{name}' due to missing rank_id.")
            skipped_count += 1
            
    print(f"Seeding complete. Created/Updated: {created_count + CaseActivityType.objects.using(db_alias).count() - created_count}, Skipped/Errors: {skipped_count}")

# --- Migration Definition ---
class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='months',
            name='month_number',
            field=models.IntegerField(help_text='The calendar month number (1-12)'),
        ),
        migrations.CreateModel(
            name='CaseActivityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)), # Keep unique=False for now
                ('description', models.TextField(blank=True, null=True)),
                ('unit_rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_types', to='statistics.unitrank')),
            ],
            options={
                'ordering': ['unit_rank', 'name'],
                # No unique_together yet
            },
        ),
        # Run data seeding *after* creating the table
        migrations.RunPython(seed_case_activity_types, reverse_code=migrations.RunPython.noop),
        # Add unique constraint *after* seeding
        migrations.AlterUniqueTogether(
            name='caseactivitytype',
            unique_together={('name', 'unit_rank')},
        ),
    ]
