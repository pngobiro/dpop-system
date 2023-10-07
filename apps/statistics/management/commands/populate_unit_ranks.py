from django.core.management.base import BaseCommand
from apps.statistics.models import UnitRank

class Command(BaseCommand):
    help = 'Populates the unit ranks table'

    def handle(self, *args, **options):
        unit_ranks = [
            {'name': 'Supreme Court', 'is_court': True},
            {'name': 'Court of Appeal', 'is_court': True},
            {'name': 'High Court', 'is_court': True},
            {'name': 'Employment and Labour Relations Court', 'is_court': True},
            {'name': 'Environment and Land Court', 'is_court': True},
            {'name': 'Magistrate Court', 'is_court': True},
            {'name': 'Kadhi Court', 'is_court': True},
            {'name': 'Tribunal', 'is_court': True},
            {'name': 'Committee', 'is_court': False},
            {'name': 'Library', 'is_court': False},
            {'name': 'Directorate', 'is_court': False},
            {'name': 'Other Office', 'is_court': False},
            {'name': 'Small Claim', 'is_court': True},
        ]

        for rank in unit_ranks:
            UnitRank.objects.create(name=rank['name'])

        self.stdout.write(self.style.SUCCESS('Successfully populated unit ranks.'))
