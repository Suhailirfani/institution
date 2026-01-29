import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

User = get_user_model()
username = 'test_admin'
user = User.objects.get(username=username)

client = Client()
client.force_login(user)

url = '/payments/list/'
print(f"Testing {url}...")
try:
    response = client.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("PASS: Payment list accessible.")
    else:
        print(f"FAIL: Status code {response.status_code}")
except Exception as e:
    print(f"Exception: {e}")
