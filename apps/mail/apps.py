      
# apps/mail/apps.py
from django.apps import AppConfig

class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mail'
    label = 'mail'

    def ready(self):
        import apps.mail.signals  # Import signals here

    