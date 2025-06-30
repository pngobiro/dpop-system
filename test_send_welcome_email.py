import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

def test_send_welcome_email(user_id, staff_username, staff_password):
    client = Client()
    # Login as staff
    login = client.login(username=staff_username, password=staff_password)
    if not login:
        print('Staff login failed. Check credentials.')
        return
    url = reverse('authentication:user_send_welcome_email', args=[user_id])
    response = client.post(url, follow=True)
    print('Status code:', response.status_code)
    print('Messages:', list(response.context['messages']))

if __name__ == '__main__':
    # Set these values for your test
    test_user_id = 2  # The user to send the welcome email to
    staff_username = 'admin'  # Staff user username
    staff_password = 'adminpassword'  # Staff user password
    test_send_welcome_email(test_user_id, staff_username, staff_password)
