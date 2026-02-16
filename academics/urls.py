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
    path("students/add/", views.StudentCreateView.as_view(), name="student_create"),
    path("students/import/", views.StudentBulkImportView.as_view(), name="student_import"),
    path("students/import/template/", views.DownloadStudentImportTemplateView.as_view(), name="student_import_template"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_update"),
    path("students/<int:pk>/certificate/", views.StudentCertificateView.as_view(), name="student_certificate"),
    path("students/<int:pk>/marksheet/", views.StudentMarksheetPDFView.as_view(), name="student_marksheet"),
    path("my-profile/", views.StudentSelfDetailView.as_view(), name="student_self_detail"),
    
    # Staff
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
    path("staff/add/", views.StaffCreateView.as_view(), name="staff_create"),
    path("staff/import/", views.StaffBulkImportView.as_view(), name="staff_import"),
    path("staff/import/template/", views.DownloadStaffImportTemplateView.as_view(), name="staff_import_template"),
    path("staff/<int:pk>/edit/", views.StaffUpdateView.as_view(), name="staff_update"),

    # Attendance
    path("attendance/add/", views.AttendanceCreateView.as_view(), name="attendance_create"),

    # Reports
    path("progress-report/<int:pk>/", views.ProgressReportView.as_view(), name="progress_report"),

    # ID Cards
    path("students/<int:pk>/id-card/", views.StudentIDCardView.as_view(), name="student_id_card"),
    path("students/id-card/bulk/", views.StudentBulkIDCardView.as_view(), name="student_id_card_bulk"),
    path("staff/<int:pk>/id-card/", views.StaffIDCardView.as_view(), name="staff_id_card"),
    path("staff/id-card/bulk/", views.StaffBulkIDCardView.as_view(), name="staff_id_card_bulk"),
    
    # Subjects
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/add/", views.SubjectCreateView.as_view(), name="subject_create"),
    
    # Exams
    path("exams/", views.ExamListView.as_view(), name="exam_list"),
    path("exams/add/", views.ExamCreateView.as_view(), name="exam_create"),
    path("exams/<int:exam_id>/subject/<int:subject_id>/entry/", views.ExamResultEntryView.as_view(), name="exam_result_entry"),
    path("exams/<int:pk>/result/", views.ClassExamResultView.as_view(), name="class_exam_result"),
]



