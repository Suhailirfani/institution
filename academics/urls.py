from django.urls import path

app_name = "academics"

from . import views

app_name = "academics"

urlpatterns = [
    # Classes
    path("classes/", views.ClassRoomListView.as_view(), name="classroom_list"),
    path("classes/add/", views.ClassRoomCreateView.as_view(), name="classroom_create"),
    path("classes/<int:pk>/", views.ClassRoomDetailView.as_view(), name="classroom_detail"),
    
    # Students
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    
    # Staff
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
    path("staff/add/", views.StaffCreateView.as_view(), name="staff_create"),

    # Attendance
    path("attendance/add/", views.AttendanceCreateView.as_view(), name="attendance_create"),

    # Reports
    path("progress-report/<int:pk>/", views.ProgressReportView.as_view(), name="progress_report"),
]



