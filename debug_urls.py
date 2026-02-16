
import os
import sys
import django
from django.urls import reverse, exceptions

# Add current directory to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adabiyya_smart_connect.settings")
django.setup()


with open("debug_output.txt", "w") as f:
    try:
        f.write("Attempting to reverse 'admissions:admission_letter'...\n")
        url = reverse('admissions:admission_letter', args=[1]) # dummy ID
        f.write(f"SUCCESS: Reversed URL: {url}\n")
    except exceptions.NoReverseMatch as e:
        f.write(f"ERROR: NoReverseMatch - {e}\n")
    except Exception as e:
        f.write(f"ERROR: {type(e).__name__} - {e}\n")

    try:
        f.write("Attempting to reverse 'admissions:dashboard'...\n")
        url = reverse('admissions:dashboard')
        f.write(f"SUCCESS: Reversed URL: {url}\n")
    except Exception as e:
        f.write(f"ERROR: {type(e).__name__} - {e}\n")

