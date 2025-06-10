from django.db import migrations

def fix_court_ranks(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    Unit = apps.get_model('statistics', 'Unit')

    # Initialize variables
    magistrate_rank_7 = None
    kadhi_court_rank = None
    tribunal_rank = None

    try:
        magistrate_rank_7 = UnitRank.objects.get(id=7, name='Magistrate Court')
    except UnitRank.DoesNotExist:
        print("Magistrate Court UnitRank with id 7 not found")
        pass

    try:
        kadhi_court_rank = UnitRank.objects.get(id=8, name='Kadhi Court')
    except UnitRank.DoesNotExist:
        print("Kadhi Court UnitRank with id 8 not found")
        pass

    try:
        tribunal_rank = UnitRank.objects.get(id=9, name='Tribunal')
    except UnitRank.DoesNotExist:
        print("Tribunal UnitRank with id 9 not found")
        pass

    # Delete duplicate Magistrate Court at ID 7
    if magistrate_rank_7:
        # Update any units pointing to ID 7 to point to ID 6
        Unit.objects.filter(unit_rank=7).update(unit_rank=6)
        magistrate_rank_7.delete()

    # Move Kadhi Court from ID 8 to ID 7
    if kadhi_court_rank:
        Unit.objects.filter(unit_rank=8).update(unit_rank=7)
        kadhi_court_rank.id = 7
        kadhi_court_rank.save()

    # Move Tribunal from ID 9 to ID 8
    if tribunal_rank:
        Unit.objects.filter(unit_rank=9).update(unit_rank=8)
        tribunal_rank.id = 8
        tribunal_rank.save()

def reverse_fix_court_ranks(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    Unit = apps.get_model('statistics', 'Unit')

    try:
        kadhi_court_rank = UnitRank.objects.get(id=7, name='Kadhi Court')
        tribunal_rank = UnitRank.objects.get(id=8, name='Tribunal')
    except UnitRank.DoesNotExist:
        return

    # Store original IDs for FK updates
    kadhi_court_id = kadhi_court_rank.id
    tribunal_id = tribunal_rank.id

    # Move Tribunal back to ID 9
    Unit.objects.filter(unit_rank=8).update(unit_rank=9)
    tribunal_rank.id = 9
    tribunal_rank.save()

    # Move Kadhi Court back to ID 8
    Unit.objects.filter(unit_rank=7).update(unit_rank=8)
    kadhi_court_rank.id = 8
    kadhi_court_rank.save()

class Migration(migrations.Migration):
    dependencies = [
        ('statistics', '0014_merge_0012_update_unit_ranks_0013_update_unit_ranks'),
    ]

    operations = [
        migrations.RunPython(fix_court_ranks, reverse_fix_court_ranks),
    ]