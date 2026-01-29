import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adabiyya_smart_connect.settings")
django.setup()

from core.models import NewsItem, JobOpening

def populate():
    # News Items
    print("Creating News Items...")
    NewsItem.objects.all().delete()
    NewsItem.objects.create(title="Admission Open for 2026-27 Academic Year", content="Applications invited for all classes.")
    NewsItem.objects.create(title="Charity Drive: Sponsor a Child Campaign Launched", content="Join us in supporting education.")
    NewsItem.objects.create(title="Result Announcement: Annual Exams 2025", content="Check results on the portal.")
    
    # Job Openings
    print("Creating Job Openings...")
    JobOpening.objects.all().delete()
    JobOpening.objects.create(
        title="High School English Teacher",
        description="We are looking for an experienced English teacher for High School classes. Minimum 3 years experience required.",
        application_link="https://forms.google.com/example"
    )
    JobOpening.objects.create(
        title="Accountant",
        description="Full-time accountant needed. Proficiency in Tally and Excel is a must.",
        # No link, should default to mailto
    )

    print("Success! Data populated.")

if __name__ == "__main__":
    populate()
