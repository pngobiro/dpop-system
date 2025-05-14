from django.db import migrations

def create_meeting_types(apps, schema_editor):
    MeetingType = apps.get_model('meetings', 'MeetingType')
    
    meeting_types = [
        {
            'name': 'Department Internal',
            'description': 'Internal meetings within a department'
        },
        {
            'name': 'With Director',
            'description': 'Meetings with department director'
        },
        {
            'name': 'Committee Meeting',
            'description': 'Committee or board meetings'
        },
        {
            'name': 'Training Session',
            'description': 'Training or workshop sessions'
        },
        {
            'name': 'Project Review',
            'description': 'Project progress review meetings'
        },
        {
            'name': 'Stakeholder Meeting',
            'description': 'Meetings with external stakeholders'
        },
        {
            'name': 'Strategy Session',
            'description': 'Strategic planning meetings'
        },
        {
            'name': 'Other',
            'description': 'Other types of meetings'
        }
    ]
    
    for mt in meeting_types:
        MeetingType.objects.create(**mt)

def remove_meeting_types(apps, schema_editor):
    MeetingType = apps.get_model('meetings', 'MeetingType')
    MeetingType.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_add_meeting_types'),
    ]

    operations = [
        migrations.RunPython(create_meeting_types, remove_meeting_types),
    ]