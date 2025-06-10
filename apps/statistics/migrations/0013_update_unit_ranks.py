from django.db import migrations
from django.db.models import F

def update_unit_ranks(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    Unit = apps.get_model('statistics', 'Unit')
    
    # Initialize variables
    elrc_rank_4 = None
    elrc_rank_5 = None
    supreme_court_rank = None
    court_of_appeal_rank = None
    high_court_rank = None
    elc_rank_5 = None
    elc_rank_6 = None
    magistrate_rank = None
    kadhi_court_rank = None
    tribunal_rank = None
    
    # Get the existing ranks
    try:
        elrc_rank_4 = UnitRank.objects.get(id=4, name='EMPLOYMENT AND LABOUR RELATIONS COURT')
    except UnitRank.DoesNotExist:
        print("ELRC UnitRank with id 4 not found")
        #return
        pass
    
    try:
        elrc_rank_5 = UnitRank.objects.get(id=5, name='EMPLOYMENT AND LABOUR RELATIONS COURT')
    except UnitRank.DoesNotExist:
        print("ELRC UnitRank with id 5 not found")
        #return
        pass

    try:
        supreme_court_rank = UnitRank.objects.get(name='Supreme Court')
    except UnitRank.DoesNotExist:
        print("Supreme Court UnitRank not found")
        return

    try:
        court_of_appeal_rank = UnitRank.objects.get(name='Court of Appeal')
    except UnitRank.DoesNotExist:
        print("Court of Appeal UnitRank not found")
        return

    try:
        high_court_rank = UnitRank.objects.get(name='High Court')
    except UnitRank.DoesNotExist:
        print("High Court UnitRank not found")
        return

    try:
        elc_rank_5 = UnitRank.objects.get(id=5, name='Environment and Land Court')
    except UnitRank.DoesNotExist:
        print("Environment and Land Court UnitRank with id 5 not found")
        return

    try:
        elc_rank_6 = UnitRank.objects.get(id=6, name='Environment and Land Court')
    except UnitRank.DoesNotExist:
        print("Environment and Land Court UnitRank with id 6 not found")
        pass

    try:
        kadhi_court_rank = UnitRank.objects.get(id=8, name='Kadhi Court')
    except UnitRank.DoesNotExist:
        print("Kadhi Court UnitRank with id 8 not found")
        return

    try:
        tribunal_rank = UnitRank.objects.get(id=9, name='Tribunal')
    except UnitRank.DoesNotExist:
        print("Tribunal UnitRank with id 9 not found")
        return

    try:
        magistrate_rank = UnitRank.objects.get(id=6, name='Magistrate Court')
    except UnitRank.DoesNotExist:
        print("Magistrate Court UnitRank with id 6 not found")
        return

    # Store the original IDs
    if supreme_court_rank:
        supreme_court_original_id = supreme_court_rank.id
    else:
        supreme_court_original_id = None

    if court_of_appeal_rank:
        court_of_appeal_original_id = court_of_appeal_rank.id
    else:
        court_of_appeal_original_id = None

    if high_court_rank:
        high_court_original_id = high_court_rank.id
    else:
        high_court_original_id = None

    if elc_rank_5:
        elc_original_id = elc_rank_5.id
    else:
        elc_original_id = None

    if magistrate_rank:
        magistrate_original_id = magistrate_rank.id
    else:
        magistrate_original_id = None

    # Update Supreme Court to ID 1
    if supreme_court_rank:
        supreme_court_rank.id = 1
        supreme_court_rank.save()

    # Update Court of Appeal to ID 2
    if court_of_appeal_rank:
        court_of_appeal_rank.id = 2
        court_of_appeal_rank.save()

    # Update High Court to ID 3
    if high_court_rank:
        high_court_rank.id = 3
        high_court_rank.save()

    # Update ELRC to ID 4
    if elrc_rank_4:
        elrc_rank_4.id = 4
        elrc_rank_4.save()

    # Delete duplicate ELC with ID 6 if it exists
    if elc_rank_6:
        # Update any units pointing to ID 6 to point to ID 5
        Unit.objects.filter(unit_rank=6).update(unit_rank=5)
        elc_rank_6.delete()

    # Keep ELC at ID 5
    if elc_rank_5:
        elc_rank_5.id = 5
        elc_rank_5.save()

    # First update Tribunal to free up ID 8
    if tribunal_rank:
        # Update any units pointing to ID 9 to temporarily point to ID 8
        Unit.objects.filter(unit_rank=9).update(unit_rank=8)
        tribunal_rank.id = 8
        tribunal_rank.save()

    # Then move Kadhi Court to ID 7
    if kadhi_court_rank:
        # Update any units pointing to ID 8 to point to ID 7
        Unit.objects.filter(unit_rank=8).update(unit_rank=7)
        kadhi_court_rank.id = 7
        kadhi_court_rank.save()

    # Delete ELRC with ID 5
    if elrc_rank_5:
        elrc_rank_5.delete()

    # Update Unit FKs
    if supreme_court_original_id:
        Unit.objects.filter(unit_rank=supreme_court_original_id).update(unit_rank=1)
    if court_of_appeal_original_id:
        Unit.objects.filter(unit_rank=court_of_appeal_original_id).update(unit_rank=2)
    if high_court_original_id:
        Unit.objects.filter(unit_rank=high_court_original_id).update(unit_rank=3)
    if elc_original_id:
        Unit.objects.filter(unit_rank=elc_original_id).update(unit_rank=5)
    if magistrate_original_id:
        Unit.objects.filter(unit_rank=magistrate_original_id).update(unit_rank=6)

def reverse_unit_ranks(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    Unit = apps.get_model('statistics', 'Unit')

    # Get the ranks
    try:
        elrc_rank = UnitRank.objects.get(name='EMPLOYMENT AND LABOUR RELATIONS COURT')
    except UnitRank.DoesNotExist:
        print("ELRC UnitRank not found")
        return
    
    try:
        supreme_court_rank = UnitRank.objects.get(name='Supreme Court')
    except UnitRank.DoesNotExist:
        print("Supreme Court UnitRank not found")
        return

    try:
        court_of_appeal_rank = UnitRank.objects.get(name='Court of Appeal')
    except UnitRank.DoesNotExist:
        print("Court of Appeal UnitRank not found")
        return

    try:
        high_court_rank = UnitRank.objects.get(name='High Court')
    except UnitRank.DoesNotExist:
        print("High Court UnitRank not found")
        return

    try:
        elc_rank = UnitRank.objects.get(id=5, name='Environment and Land Court')
    except UnitRank.DoesNotExist:
        print("Environment and Land Court UnitRank with id 5 not found")
        return

    try:
        magistrate_rank = UnitRank.objects.get(id=6, name='Magistrate Court')
    except UnitRank.DoesNotExist:
        print("Magistrate Court UnitRank with id 6 not found")
        return

    try:
        kadhi_court_rank = UnitRank.objects.get(id=7, name='Kadhi Court')
    except UnitRank.DoesNotExist:
        print("Kadhi Court UnitRank with id 7 not found")
        return

    try:
        tribunal_rank = UnitRank.objects.get(id=8, name='Tribunal')
    except UnitRank.DoesNotExist:
        print("Tribunal UnitRank with id 8 not found")
        return

    # Store the current IDs
    elrc_current_id = elrc_rank.id
    supreme_court_current_id = supreme_court_rank.id
    court_of_appeal_current_id = court_of_appeal_rank.id
    high_court_current_id = high_court_rank.id
    elc_current_id = elc_rank.id
    magistrate_current_id = magistrate_rank.id
    kadhi_court_current_id = kadhi_court_rank.id
    tribunal_current_id = tribunal_rank.id

    # Reverse the IDs
    elrc_rank.id = 4
    elrc_rank.save()

    court_of_appeal_rank.id = court_of_appeal_current_id
    court_of_appeal_rank.save()

    high_court_rank.id = high_court_current_id
    high_court_rank.save()

    supreme_court_rank.id = supreme_court_current_id
    supreme_court_rank.save()

    # Restore ELC to ID 5 if needed
    if elc_rank.id != 5:
        elc_rank.id = 5
        elc_rank.save()

    # Move Magistrate Court back to ID 7
    if magistrate_rank.id == 6:
        Unit.objects.filter(unit_rank=6).update(unit_rank=7)
        magistrate_rank.id = 7
        magistrate_rank.save()

    # Update Unit FKs
    # Restore Kadhi Court and Tribunal to original IDs
    kadhi_court_rank.id = 8
    kadhi_court_rank.save()
    
    tribunal_rank.id = 9
    tribunal_rank.save()

    # Restore original Unit FKs
    Unit.objects.filter(unit_rank=1).update(unit_rank=supreme_court_current_id)
    Unit.objects.filter(unit_rank=2).update(unit_rank=court_of_appeal_current_id)
    Unit.objects.filter(unit_rank=3).update(unit_rank=high_court_current_id)
    Unit.objects.filter(unit_rank=4).update(unit_rank=elrc_current_id)
    Unit.objects.filter(unit_rank=5).update(unit_rank=elc_current_id)
    Unit.objects.filter(unit_rank=7).update(unit_rank=kadhi_court_current_id)
    Unit.objects.filter(unit_rank=8).update(unit_rank=tribunal_current_id)

class Migration(migrations.Migration):
    dependencies = [
        ('statistics', '0011_update_unit_ranks'),
    ]

    operations = [
        migrations.RunPython(update_unit_ranks, reverse_unit_ranks),
    ]