from django.db import migrations
from django.db.models import F

def update_unit_ranks(apps, schema_editor):
    UnitRank = apps.get_model('statistics', 'UnitRank')
    Unit = apps.get_model('statistics', 'Unit')
    
    # Get the existing ranks
    try:
        elrc_rank_4 = UnitRank.objects.get(id=4, name__icontains='EMPLOYMENT AND LABOUR RELATIONS COURT')
    except UnitRank.DoesNotExist:
        print("ELRC UnitRank with id 4 not found")
        #return
        pass
    
    try:
        elrc_rank_5 = UnitRank.objects.get(id=5, name__icontains='EMPLOYMENT AND LABOUR RELATIONS COURT')
    except UnitRank.DoesNotExist:
        print("ELRC UnitRank with id 5 not found")
        #return
        pass

    try:
        supreme_court_rank = UnitRank.objects.get(name__icontains='Supreme Court')
    except UnitRank.DoesNotExist:
        print("Supreme Court UnitRank not found")
        return

    try:
        court_of_appeal_rank = UnitRank.objects.get(name__icontains='Court of Appeal')
    except UnitRank.DoesNotExist:
        print("Court of Appeal UnitRank not found")
        return

    try:
        high_court_rank = UnitRank.objects.get(name__icontains='High Court')
    except UnitRank.DoesNotExist:
        print("High Court UnitRank not found")
        return

    try:
        elc_rank = UnitRank.objects.get(name__icontains='Environment and Land Court')
    except UnitRank.DoesNotExist:
        print("Environment and Land Court UnitRank not found")
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

    if elc_rank:
        elc_original_id = elc_rank.id
    else:
        elc_original_id = None

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

    # Update ELC to ID 5
    if elc_rank:
        elc_rank.id = 5
        elc_rank.save()

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
        elc_rank = UnitRank.objects.get(name='Environment and Land Court')
    except UnitRank.DoesNotExist:
        print("Environment and Land Court UnitRank not found")
        return

    # Store the current IDs
    elrc_current_id = elrc_rank.id
    supreme_court_current_id = supreme_court_rank.id
    court_of_appeal_current_id = court_of_appeal_rank.id
    high_court_current_id = high_court_rank.id
    elc_current_id = elc_rank.id

    # Reverse the IDs
    elrc_rank.id = 1
    elrc_rank.save()

    court_of_appeal_rank.id = court_of_appeal_current_id
    court_of_appeal_rank.save()

    high_court_rank.id = high_court_current_id
    high_court_rank.save()

    supreme_court_rank.id = supreme_court_current_id
    supreme_court_rank.save()

    elc_rank.id = 5
    elc_rank.save()

    # Update Unit FKs
    Unit.objects.filter(unit_rank=elrc_current_id).update(unit_rank=1)
    Unit.objects.filter(unit_rank=court_of_appeal_current_id).update(unit_rank=court_of_appeal_original_id)
    Unit.objects.filter(unit_rank=high_court_current_id).update(unit_rank=high_court_original_id)
    Unit.objects.filter(unit_rank=supreme_court_current_id).update(unit_rank=supreme_court_original_id)
    Unit.objects.filter(unit_rank=elc_current_id).update(unit_rank=elc_original_id)

class Migration(migrations.Migration):
    dependencies = [
        ('statistics', '0011_update_unit_ranks'),
    ]

    operations = [
        migrations.RunPython(update_unit_ranks, reverse_unit_ranks),
    ]