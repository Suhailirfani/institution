import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first() or User.objects.create(username='mock')

factory = RequestFactory()
request = factory.get('/')
request.user = user

context = {
    'staff_members': [],
    'user': user,
    'request': request
}

print("Rendering staff_list.html...")
try:
    rendered = render_to_string('academics/staff_list.html', context, request=request)
    print("Render Success!")
except Exception as e:
    print(f"Render Failed: {e}")
