from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from core.views import RoleRequiredMixin
from core.services import NotificationService
from .models import ClassRoom, StudentProfile, StaffProfile, AttendanceRecord, ExamResult
from django.contrib import messages
from django.views.generic import FormView
from .forms import (
    ClassRoomForm, StudentProfileForm, StaffCreationForm, StudentCreationForm, 
    StudentUpdateForm, StudentBulkImportForm, StaffUpdateForm, StaffBulkImportForm
)
import openpyxl
from django.contrib import messages
from django.views.generic import FormView

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

class StudentCreateView(RoleRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentCreationForm
    template_name = "academics/student_form.html"
    success_url = reverse_lazy('academics:student_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Add New Student")
        return context

class StudentUpdateView(RoleRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentUpdateForm
    template_name = "academics/student_form.html"
    success_url = reverse_lazy('academics:student_list')
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update Student Profile")
        return context

class StudentSelfDetailView(LoginRequiredMixin, DetailView):
    model = StudentProfile
    template_name = "academics/student_detail.html" # Reusing detail template
    context_object_name = 'student'

    def get_object(self, queryset=None):
        if hasattr(self.request.user, 'student_profile'):
            return self.request.user.student_profile
        return None # Should handle 404 or redirect nicely

class StudentBulkImportView(RoleRequiredMixin, FormView):
    template_name = "academics/student_import.html"
    form_class = StudentBulkImportForm
    success_url = reverse_lazy('academics:student_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Bulk Import Students")
        return context

    def form_valid(self, form):
        excel_file = self.request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        
        # Assume header is row 1
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        
        created_count = 0
        errors = []
        
        for index, row in enumerate(rows, start=2):
            # Columns: First Name, Last Name, Email, DOB, Admin No, WhatsApp, Class Code, Father Name, Mother Name, Address, Blood Group
            try:
                # Pad row with None if it's shorter than expected
                row = list(row) + [None] * (11 - len(row))
                first_name, last_name, email, dob, admission_number, whatsapp_number, class_code, father_name, mother_name, address, blood_group = row[:11]
                
                if not all([first_name, email, admission_number, class_code]):
                    continue # Validating mandatory fields only

                if StudentProfile.objects.filter(admission_number=admission_number).exists():
                    errors.append(f"Row {index}: Student with admission number {admission_number} already exists.")
                    continue
                    
                if User.objects.filter(email=email).exists():
                    errors.append(f"Row {index}: User with email {email} already exists.")
                    continue

                # Find classroom (Assuming Subject Code logic, but here we need Class Code which isn't unique without Institution... 
                # For MVP, let's assume Class Code maps to Standard + Division or verify strictly)
                # Actually, earlier models didn't have strict 'code' for class. Let's assume input is Standard (e.g. "10 A")
                # Wait, ClassRoom has `standard` and `division`.
                # Simplification: Assume input is "Standard-Division" e.g. "10-A"
                if '-' in str(class_code):
                     std, div = str(class_code).split('-', 1)
                     classroom = ClassRoom.objects.filter(standard__iexact=std.strip(), division__iexact=div.strip()).first()
                else:
                     classroom = ClassRoom.objects.filter(standard__iexact=str(class_code).strip()).first()

                if not classroom:
                    errors.append(f"Row {index}: Class '{class_code}' not found.")
                    continue

                # Create User
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password="password123", # Default password, should force change later
                    first_name=first_name,
                    last_name=last_name,
                    role=User.Roles.STUDENT
                )
                
                # Create Profile
                StudentProfile.objects.create(
                    user=user,
                    admission_number=admission_number,
                    whatsapp_number=whatsapp_number,
                    date_of_birth=dob,
                    classroom=classroom,
                    father_name=father_name or "",
                    mother_name=mother_name or "",
                    address=address or "",
                    blood_group=blood_group or ""
                )
                created_count += 1
                
            except Exception as e:
                errors.append(f"Row {index}: Error processing - {str(e)}")

        if created_count > 0:
            messages.success(self.request, f"Successfully imported {created_count} students.")
        
        if errors:
            messages.warning(self.request, f"Encoutered {len(errors)} errors. Check below.")
            # Pass errors to template? Or just flash huge message.
            # Ideally context, but redirects clear context. Using messages for now.
            for err in errors[:5]: # Show first 5 errors
                 messages.error(self.request, err)
            if len(errors) > 5:
                messages.error(self.request, f"...and {len(errors)-5} more errors.")
                
        return super().form_valid(form)


class DownloadStudentImportTemplateView(RoleRequiredMixin, View):
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]

    def get(self, request, *args, **kwargs):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Student Import Template"
        
        # Headers
        headers = ["First Name", "Last Name", "Email", "Date of Birth (YYYY-MM-DD)", "Admission Number", "WhatsApp Number", "Class Code", "Father Name", "Mother Name", "Address", "Blood Group"]
        ws.append(headers)
        
        # Sample Row
        ws.append(["John", "Doe", "john.doe@example.com", "2010-05-15", "ADM001", "9876543210", "10-A", "John Doe Sr.", "Jane Doe", "123 Street, City", "O+"])
        
        # Adjust column widths
        for col in range(1, len(headers) + 1):
             ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 20

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=student_import_template.xlsx'
        
        wb.save(response)
        return response


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

class StaffUpdateView(RoleRequiredMixin, UpdateView):
    model = StaffProfile
    form_class = StaffUpdateForm
    template_name = "academics/staff_form.html"
    success_url = reverse_lazy('academics:staff_list')
    allowed_roles = [User.Roles.ADMIN]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Edit Staff")
        return context

class StaffBulkImportView(RoleRequiredMixin, FormView):
    template_name = "academics/staff_import.html"
    form_class = StaffBulkImportForm
    success_url = reverse_lazy('academics:staff_list')
    allowed_roles = [User.Roles.ADMIN]

    def form_valid(self, form):
        excel_file = form.cleaned_data['excel_file']
        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            rows = list(ws.iter_rows(values_only=True))
            
            if not rows or len(rows) < 2:
                messages.error(self.request, "The Excel file is empty or missing headers.")
                return self.form_invalid(form)

            # Skip header
            created_count = 0
            errors = []
            
            from core.models import Institution
            # For this MVP, assign to first institution or let user pick, assuming 1 for now
            institution = Institution.objects.first()

            for index, row in enumerate(rows, start=2):
                # Columns: First Name, Last Name, Email, Mobile, Place, Department, Designation, Qualification
                try:
                    # Pad row
                    row = list(row) + [None] * (8 - len(row))
                    first_name, last_name, email, mobile, place, department, designation, qualification = row[:8]
                    
                    if not all([first_name, email, mobile, place]):
                        continue # Skip if compulsory fields are missing

                    if User.objects.filter(email=email).exists():
                        errors.append(f"Row {index}: User with email {email} already exists.")
                        continue

                    # Create User
                    user = User.objects.create_user(
                        email=email,
                        username=email, # Use email as username
                        password="defaultpassword123", # Set a default password
                        first_name=first_name,
                        last_name=last_name,
                        role=User.Roles.STAFF
                    )
                    
                    # Create Profile
                    StaffProfile.objects.create(
                        user=user,
                        institution=institution,
                        mobile_number=mobile,
                        place=place,
                        department=department or "",
                        designation=designation or "",
                        qualification=qualification or ""
                    )
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index}: Error - {str(e)}")
            
            if created_count > 0:
                messages.success(self.request, f"Successfully imported {created_count} staff members.")
            
            if errors:
                for error in errors[:10]: # Limit errors shown
                    messages.warning(self.request, error)
                if len(errors) > 10:
                    messages.warning(self.request, f"And {len(errors) - 10} more errors.")
                    
        except Exception as e:
            messages.error(self.request, f"Error processing file: {str(e)}")
            return self.form_invalid(form)
            
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Bulk Import Staff")
        return context

class DownloadStaffImportTemplateView(RoleRequiredMixin, View):
    allowed_roles = [User.Roles.ADMIN]

    def get(self, request, *args, **kwargs):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Staff Import Template"
        
        # Headers
        headers = ["First Name", "Last Name", "Email", "Mobile", "Place", "Department", "Designation", "Qualification"]
        ws.append(headers)
        
        # Sample Row
        ws.append(["Jane", "Smith", "jane.smith@example.com", "9876543210", "New York", "Science", "Teacher", "M.Sc B.Ed"])
        
        # Adjust column widths
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 20
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=staff_import_template.xlsx'
        
        wb.save(response)
        return response

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

class StudentCertificateView(RoleRequiredMixin, DetailView):
    model = StudentProfile
    template_name = "academics/student_certificate.html"
    context_object_name = 'student'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Try to get the institution from the student's classroom, or fallback to the first active one
        if self.object.classroom and self.object.classroom.institution:
             context['institution'] = self.object.classroom.institution
        else:
             from core.models import Institution
             context['institution'] = Institution.objects.filter(is_active=True).first()
        return context
