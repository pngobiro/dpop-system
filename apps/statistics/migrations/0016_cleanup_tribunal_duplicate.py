from django.db import migrations

def cleanup_tribunal_duplicate(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    Unit = apps.get_model('statistics', 'Unit')

    try:
        tribunal_rank_9 = UnitRank.objects.get(id=9, name='Tribunal')
        # Update any units pointing to ID 9 to point to ID 8
        Unit.objects.filter(unit_rank=9).update(unit_rank=8)
        tribunal_rank_9.delete()
    except UnitRank.DoesNotExist:
        print("Tribunal UnitRank with id 9 not found")
        pass

def reverse_cleanup_tribunal_duplicate(apps, schema_editor):
    # No need to reverse this operation as it's just cleanup
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('statistics', '0015_fix_court_ranks'),
    ]

    operations = [
        migrations.RunPython(cleanup_tribunal_duplicate, reverse_cleanup_tribunal_duplicate),
    ]