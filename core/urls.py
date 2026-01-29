from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    # Public website
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("institutions/", views.InstitutionsView.as_view(), name="institutions"),
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
]



