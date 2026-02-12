from django.urls import path

from . import views

app_name = "core"
# Force reload

urlpatterns = [
    # Public website
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("institutions/", views.InstitutionsView.as_view(), name="institutions"),
    path("institutions/<int:pk>/", views.InstitutionDetailView.as_view(), name="institution_detail"),
    path("admissions/", views.AdmissionsInfoView.as_view(), name="admissions_info"),
    path("charity/", views.CharityWingView.as_view(), name="charity"),
    path("career/", views.CareerView.as_view(), name="career"),
    path("contact/", views.ContactView.as_view(), name="contact"),

    # Role-based dashboards
    path("dashboard/", views.DashboardRouterView.as_view(), name="dashboard_router"),
    path("dashboard/admin/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path("dashboard/staff/", views.StaffDashboardView.as_view(), name="staff_dashboard"),
    path("dashboard/student/", views.StudentDashboardView.as_view(), name="student_dashboard"),
    path("dashboard/parent/", views.ParentDashboardView.as_view(), name="parent_dashboard"),
    path("dashboard/sponsor/", views.SponsorDashboardView.as_view(), name="sponsor_dashboard"),
    path("dashboard/committee/", views.CommitteeDashboardView.as_view(), name="committee_dashboard"),
    
    # Academic Year Management
    path("academic-years/", views.AcademicYearListView.as_view(), name="academicyear_list"),
    path("academic-years/add/", views.AcademicYearCreateView.as_view(), name="academicyear_create"),
    path("academic-years/<int:pk>/edit/", views.AcademicYearUpdateView.as_view(), name="academicyear_update"),

    # Institution Management
    path("institutions/manage/", views.InstitutionManagementListView.as_view(), name="institution_manage"),
    path("institutions/add/", views.InstitutionCreateView.as_view(), name="institution_create"),
    path("institutions/<int:pk>/edit/", views.InstitutionUpdateView.as_view(), name="institution_update"),
    # Job Applications
    path("career/apply/<int:job_id>/", views.JobApplicationCreateView.as_view(), name="job_application_create"),
    path("career/success/", views.JobApplicationSuccessView.as_view(), name="job_application_success"),
    path("dashboard/admin/applications/", views.JobApplicationListView.as_view(), name="job_application_list"),
    path("dashboard/admin/applications/<int:pk>/review/", views.JobApplicationUpdateView.as_view(), name="job_application_review"),
    
    # Update History
    path("updates/", views.UpdateHistoryView.as_view(), name="update_history"),
]



