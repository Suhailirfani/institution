import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

User = get_user_model()

def verify_modules():
    client = Client()
    
    # 1. Create Test User
    username = 'test_admin'
    password = 'test_password'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username, 'admin@example.com', password)
        print(f"Created user: {username}")
    else:
        user = User.objects.get(username=username)
        # reset password to ensure login works
        user.set_password(password)
        user.save()
        print(f"Using existing user: {username}")

    # 2. Login
    login_successful = client.login(username=username, password=password)
    if login_successful:
        print("Login Successful")
    else:
        print("Login Failed")
        return

    # 3. Define URLs to test
    urls_to_test = [
        # Public
        '/',
        '/about/',
        '/admissions/apply/',
        
        # Accounts
        '/accounts/profile/',
        
        # Admissions
        '/admissions/applications/',
        
        # Academics
        '/academics/classes/',
        '/academics/students/',
        '/academics/staff/',
    ]

    # 4. Check URLs
    print("\n--- Verifying URLs ---")
    all_passed = True
    for url in urls_to_test:
        try:
            response = client.get(url)
            status = response.status_code
            if status == 200:
                print(f"[PASS] {url} - 200 OK")
            else:
                print(f"[FAIL] {url} - {status}")
                all_passed = False
        except Exception as e:
            print(f"[ERROR] {url} - {str(e)}")
            all_passed = False

    if all_passed:
        print("\nVerification PASSED: All core modules are accessible.")
    else:
        print("\nVerification FAILED: Some modules are not working correctly.")

if __name__ == "__main__":
    verify_modules()
