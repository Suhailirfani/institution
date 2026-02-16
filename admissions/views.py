from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from accounts.models import User
from core.views import RoleRequiredMixin
from .models import AdmissionApplication
from .forms import AdmissionApplicationForm, AdmissionReviewForm

class AdmissionApplicationCreateView(LoginRequiredMixin, CreateView):
    model = AdmissionApplication
    form_class = AdmissionApplicationForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('admissions:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Apply for Admission")
        context['page_icon'] = "bi-mortarboard"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, _("Application submitted successfully!"))
        return super().form_valid(form)

class ApplicantDashboardView(LoginRequiredMixin, ListView):
    model = AdmissionApplication
    template_name = "admissions/dashboard.html"
    context_object_name = 'applications'

    def get_queryset(self):
        return AdmissionApplication.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("My Applications")
        return context

class AdmissionApplicationListView(RoleRequiredMixin, ListView):
    model = AdmissionApplication
    template_name = "components/data_table.html" # Reusing data table component via wrapper or context
    context_object_name = 'applications'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Setup for data_table.html
        context['table_title'] = _("Admission Applications")
        context['columns'] = [
             {'header': 'Applicant', 'field': 'full_name'},
             {'header': 'Programme', 'field': 'programme'},
             {'header': 'Status', 'field': 'status'},
             {'header': 'Date', 'field': 'submitted_at'},
             {'header': 'Action', 'field': 'action'}, # Placeholder for loop logic in template
        ]
        # Since data_table.html is a component, we might need a wrapper template
        # checking "templates/admissions/application_list.html" first.
        # But for now, I'll use a custom template that includes the component.
        self.template_name = "admissions/application_list.html" 
        return context

from django.utils import timezone

class AdmissionApplicationDetailView(RoleRequiredMixin, UpdateView):
    model = AdmissionApplication
    form_class = AdmissionReviewForm
    template_name = "admissions/application_detail_admin.html"
    context_object_name = 'application'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]
    success_url = reverse_lazy('admissions:application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Review Application: {self.object.full_name}"
        context['page_icon'] = "bi-clipboard-check"
        return context

    def form_valid(self, form):
        form.instance.reviewed_by = self.request.user
        form.instance.reviewed_at = timezone.now()
        messages.success(self.request, _("Application status updated."))
        return super().form_valid(form)

from .forms import StudentEnrollmentForm
from academics.models import StudentProfile

class EnrollStudentView(RoleRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentEnrollmentForm
    template_name = "core/generic_form.html"
    allowed_roles = [User.Roles.ADMIN]
    
    def dispatch(self, request, *args, **kwargs):
        self.application = AdmissionApplication.objects.get(pk=self.kwargs.get('pk'))
        if not self.application.user:
            messages.error(request, "This application is not linked to a user account.")
            return redirect('admissions:application_detail', pk=self.application.pk)
        if hasattr(self.application.user, 'student_profile'):
             messages.warning(request, "This user is already enrolled as a student.")
             return redirect('admissions:application_detail', pk=self.application.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        app = self.application
        initial.update({
            'father_name': app.guardian_name, # Approximation
            'address': app.address,
            'date_of_birth': app.date_of_birth,
            # 'classroom': ... admin selects this
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Enroll Student: {self.application.full_name}"
        context['page_icon'] = "bi-person-check"
        return context

    def form_valid(self, form):
        form.instance.user = self.application.user
        student = form.save()
        
        # Update User Role
        user = self.application.user
        user.role = User.Roles.STUDENT
        user.save()
        
        # Update Application Status
        self.application.status = AdmissionApplication.Status.APPROVED
        self.application.save()
        
        messages.success(self.request, f"Student {student} enrolled successfully!")
        return redirect('admissions:application_detail', pk=self.application.pk)

# --- Programme Management ---
from .models import Programme
from .forms import ProgrammeForm

class ProgrammeListView(RoleRequiredMixin, ListView):
    model = Programme
    template_name = "admissions/programme_list.html"
    context_object_name = 'programmes'
    allowed_roles = [User.Roles.ADMIN]

    def get_queryset(self):
        queryset = super().get_queryset()
        institution_id = self.request.GET.get('institution')
        if institution_id:
            queryset = queryset.filter(institution_id=institution_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('institution'):
            from core.models import Institution
            context['current_institution'] = Institution.objects.get(pk=self.request.GET.get('institution'))
        return context

class ProgrammeCreateView(RoleRequiredMixin, CreateView):
    model = Programme
    form_class = ProgrammeForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('admissions:programme_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_initial(self):
        initial = super().get_initial()
        institution_id = self.request.GET.get('institution')
        if institution_id:
            initial['institution'] = institution_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Add Programme")
        return context

class ProgrammeUpdateView(RoleRequiredMixin, UpdateView):
    model = Programme
    form_class = ProgrammeForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('admissions:programme_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update Programme")
        return context

from django.views.generic import DeleteView
class ProgrammeDeleteView(RoleRequiredMixin, DeleteView):
    model = Programme
    success_url = reverse_lazy('admissions:programme_list')
    template_name = "core/confirm_delete.html"
    allowed_roles = [User.Roles.ADMIN]

from django.views.generic import View
from django.http import HttpResponse
from core.utils import render_to_pdf
import datetime

class AdmissionLetterView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            application = AdmissionApplication.objects.select_related('user', 'programme').get(pk=pk, user=request.user)
        except AdmissionApplication.DoesNotExist:
            messages.error(request, _("Application not found."))
            return redirect('admissions:dashboard')

        if application.status != AdmissionApplication.Status.APPROVED:
            messages.error(request, _("Admission letter is only available for approved applications."))
            return redirect('admissions:dashboard')

        # Get student profile for Roll No (Admission Number)
        roll_no = "N/A"
        admission_date = application.updated_at if hasattr(application, 'updated_at') else datetime.date.today() # Fallback
        
        if hasattr(application.user, 'student_profile'):
            roll_no = application.user.student_profile.admission_number
            # Use student profile created date as admission date if available
            if hasattr(application.user.student_profile, 'date_of_joining'):
                 admission_date = application.user.student_profile.date_of_joining

        # Reporting info (hardcoded for now as per request)
        reporting_date = datetime.date.today() + datetime.timedelta(days=7) # Example: 1 week from now
        reporting_time = datetime.time(9, 0) # 9:00 AM

        context = {
            'application': application,
            'roll_no': roll_no,
            'admission_date': admission_date,
            'reporting_date': reporting_date,
            'reporting_time': reporting_time,
        }

        pdf = render_to_pdf('admissions/pdf/admission_letter.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Admission_Letter_{application.id}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        return HttpResponse("Error generating PDF", status=500)
