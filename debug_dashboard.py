import os
import django
from django.template.loader import render_to_string
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first() or User.objects.create(username='mock')

factory = RequestFactory()
request = factory.get('/dashboard/admin/')
request.user = user

# Mock context usually provided by AdminDashboardView
context = {
    'total_students': 100,
    'total_staff': 20,
    'pending_applications': 5,
    'total_applications': 50,
    'total_payments': 10,
    'total_revenue': 1000.00,
    'active_sponsorships': 2,
    'user': user
}

print("Rendering dashboard_admin.html...")
try:
    rendered = render_to_string('core/dashboard_admin.html', context, request=request)
    if "{% include" in rendered:
        print("FAIL: Found raw template tag in output!")
        # Find exactly where
        start = rendered.find("{% include")
        print(f"Context: {rendered[start:start+200]}")
    else:
        print("SUCCESS: Template rendered without raw tags.")
except Exception as e:
    print(f"Render Failed: {e}")
