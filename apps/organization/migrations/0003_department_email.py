from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_role_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]