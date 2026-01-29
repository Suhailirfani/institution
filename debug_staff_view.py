import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

User = get_user_model()
username = 'test_admin'
user = User.objects.get(username=username)

client = Client()
client.force_login(user)

# Data Validation
from academics.models import StaffProfile
print(f"Staff Count: {StaffProfile.objects.count()}")
for staff in StaffProfile.objects.all():
    try:
        print(f"Staff: {staff}, Inst: {staff.institution.name}")
    except Exception as e:
        print(f"Data Error on staff {staff.pk}: {e}")

url = '/academics/staff/'
print(f"Testing {url}...")
try:
    response = client.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        content = response.content.decode('utf-8')
        if "Exception Value" in content:
            start = content.find("Exception Value")
            print("FOUND ERROR:")
            print(content[start:start+300])
        else:
            print("Error page content (head):")
            print(content[:500])
except Exception as e:
    print(f"Exception: {e}")
