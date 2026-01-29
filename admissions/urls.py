from django.urls import path

app_name = "admissions"

from . import views

app_name = "admissions"

urlpatterns = [
    path("apply/", views.AdmissionApplicationCreateView.as_view(), name="apply"),
    path("applications/", views.AdmissionApplicationListView.as_view(), name="application_list"),
    path("applications/<int:pk>/", views.AdmissionApplicationDetailView.as_view(), name="application_detail"),
]



