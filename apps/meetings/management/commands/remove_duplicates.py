from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.meetings.models import Meeting

class Command(BaseCommand):
    help = 'Remove duplicate meetings'

    def handle(self, *args, **options):
        # Find duplicate sets
        dupes = Meeting.objects.values('date', 'title', 'department', 'organizer')\
                              .annotate(count=Count('id'))\
                              .filter(count__gt=1)
        
        removed = 0
        for d in dupes:
            # Get all meetings in this duplicate set
            meetings = Meeting.objects.filter(
                date=d['date'],
                title=d['title'],
                department=d['department'],
                organizer=d['organizer']
            ).order_by('id')
            
            # Keep the first one, delete the rest
            for m in meetings[1:]:
                m.delete()
                removed += 1
        
        self.stdout.write(f'Removed {removed} duplicate meetings.')