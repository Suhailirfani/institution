import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

client = Client()

url = '/admissions/apply/'
print(f"Testing {url}...")
try:
    response = client.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        content = response.content.decode('utf-8')
        if "Exception Value" in content:
            start = content.find("Exception Value")
            print("FOUND ERROR:")
            print(content[start:start+500])
        else:
            print("Error page content (head):")
            print(content[:500])
            # also print tail in case it's there
            print(content[-500:])
except Exception as e:
    print(f"Exception: {e}")
