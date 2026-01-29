from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from core.views import RoleRequiredMixin
from core.services import NotificationService
from .models import ClassRoom, StudentProfile, StaffProfile, AttendanceRecord, ExamResult
from .forms import ClassRoomForm, StudentProfileForm, StaffCreationForm

# --- Class Room Views ---
class ClassRoomListView(RoleRequiredMixin, ListView):
    model = ClassRoom
    template_name = "academics/classroom_list.html"
    context_object_name = 'classrooms'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]

    def get_queryset(self):
        return ClassRoom.objects.select_related('academic_year').annotate(student_count=Count('students'))

class ClassRoomDetailView(RoleRequiredMixin, DetailView):
    model = ClassRoom
    template_name = "academics/classroom_detail.html"
    context_object_name = 'classroom'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = self.object.students.all().select_related('user')
        return context

class ClassRoomCreateView(RoleRequiredMixin, CreateView):
    model = ClassRoom
    form_class = ClassRoomForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('academics:classroom_list')
    allowed_roles = [User.Roles.ADMIN] # Only admin creates classes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Add New Class")
        return context

# --- Student Views ---
class StudentListView(RoleRequiredMixin, ListView):
    model = StudentProfile
    template_name = "academics/student_list.html"
    context_object_name = 'students'
    paginate_by = 20
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]

    def get_queryset(self):
        return StudentProfile.objects.select_related('user', 'classroom').order_by('classroom__standard', 'user__first_name')

class StudentDetailView(RoleRequiredMixin, DetailView):
    model = StudentProfile
    template_name = "academics/student_detail.html"
    context_object_name = 'student'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]

# --- Staff Views ---
class StaffListView(RoleRequiredMixin, ListView):
    model = StaffProfile
    template_name = "academics/staff_list.html"
    context_object_name = 'staff_members'
    allowed_roles = [User.Roles.ADMIN]

class StaffCreateView(RoleRequiredMixin, CreateView):
    model = StaffProfile
    form_class = StaffCreationForm
    template_name = "academics/staff_form.html"
    success_url = reverse_lazy('academics:staff_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Add New Staff Member")
        return context

# --- Attendance Views ---
class AttendanceCreateView(RoleRequiredMixin, CreateView):
    model = AttendanceRecord
    fields = ['student', 'date', 'status']  # distinct from bulk entry for MVP simplicity
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('academics:student_list') # Redirect somewhere useful
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]

    def form_valid(self, form):
        response = super().form_valid(form)
        # Check if absent and send alert
        if self.object.status == AttendanceRecord.Status.ABSENT:
            NotificationService.send_attendance_alert(
                student=self.object.student,
                date=self.object.date,
                status=self.object.status
            )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Mark Student Attendance")
        return context

# --- Exam / Reports Views ---
class ProgressReportView(RoleRequiredMixin, DetailView):
    model = StudentProfile
    template_name = "academics/progress_report.html"
    context_object_name = 'student'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF, User.Roles.PARENT, User.Roles.STUDENT]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all results for this student
        results = ExamResult.objects.filter(student=self.object).select_related('exam', 'subject')
        
        # Group by Exam
        exams_data = {}
        for res in results:
            if res.exam not in exams_data:
                exams_data[res.exam] = {
                    'exam': res.exam,
                    'results': [],
                    'total_marks': 0,
                    'max_total': 0
                }
            exams_data[res.exam]['results'].append(res)
            exams_data[res.exam]['total_marks'] += res.marks_obtained
            exams_data[res.exam]['max_total'] += res.max_marks
            
        context['exams_data'] = exams_data.values()
        return context
