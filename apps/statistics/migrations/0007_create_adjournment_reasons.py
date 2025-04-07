from django.db import migrations, models
import django.db.models.deletion

def create_elrc_adjournment_reasons(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    AdjournmentReason = apps.get_model('statistics', 'AdjournmentReason')
    
    # Get ELRC rank (assuming rank 4 is ELRC)
    elrc_rank = UnitRank.objects.get(id=4)  
    
    # Create adjournment reasons
    reasons = [
        "Advocate not present",
        "Advocate not ready",
        "Court on its own motion",
        "Death of a party",
        "Expert report not ready",
        "File missing",
        "Judgment not ready",
        "Judicial officer on transfer",
        "Matter not cause listed",
        "No proof of service",
        "No reason recorded",
        "Partie(s) not present",
        "Partie(s) not ready",
        "Parties to Negotiate",
        "Ruling not ready",
        "Submissions not ready",
        "Typed proceedings not ready",
        "Witness not present",
        "Witness not ready",
        "Court Indisposed",
        "Public Holiday"
    ]
    
    for reason in reasons:
        AdjournmentReason.objects.create(
            name=reason,
            unit_rank=elrc_rank
        )

class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0006_create_case_outcomes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjournmentReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjournment_reasons', to='statistics.UnitRank')),
            ],
            options={
                'verbose_name_plural': 'Adjournment Reasons',
                'ordering': ['unit_rank', 'name'],
                'unique_together': {('name', 'unit_rank')},
            },
        ),
        migrations.RunPython(create_elrc_adjournment_reasons),
    ]