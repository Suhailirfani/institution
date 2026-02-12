from django.urls import path

app_name = "admissions"

from . import views

app_name = "admissions"

urlpatterns = [
    path("dashboard/", views.ApplicantDashboardView.as_view(), name="dashboard"),
    path("apply/", views.AdmissionApplicationCreateView.as_view(), name="apply"),
    path("applications/", views.AdmissionApplicationListView.as_view(), name="application_list"),
    path("applications/<int:pk>/", views.AdmissionApplicationDetailView.as_view(), name="application_detail"),
    path("applications/<int:pk>/enroll/", views.EnrollStudentView.as_view(), name="application_enroll"),
    
    # Programme Management
    path("programmes/", views.ProgrammeListView.as_view(), name="programme_list"),
    path("programmes/add/", views.ProgrammeCreateView.as_view(), name="programme_create"),
    path("programmes/<int:pk>/edit/", views.ProgrammeUpdateView.as_view(), name="programme_update"),
    path("programmes/<int:pk>/delete/", views.ProgrammeDeleteView.as_view(), name="programme_delete"),
]



