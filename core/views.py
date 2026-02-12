from django.db import models
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, ListView, DetailView, CreateView, UpdateView

from accounts.models import User
from accounts.permissions import RoleRequiredMixin
from admissions.models import AdmissionApplication
from academics.models import StudentProfile, StaffProfile
from payments.models import Payment
from sponsorship.models import SponsorshipAllocation
from .models import NewsItem, JobOpening, AcademicYear, Institution, JobApplication
from .forms import AcademicYearForm, InstitutionForm, JobApplicationForm


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_items"] = NewsItem.objects.filter(is_active=True)
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class InstitutionsView(TemplateView):
    template_name = "core/institutions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Institution
        context["institutions"] = Institution.objects.filter(is_active=True).order_by('id')
        return context


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = "core/institution_detail.html"
    context_object_name = "institution"

    def get_queryset(self):
        return Institution.objects.filter(is_active=True)


class AdmissionsInfoView(TemplateView):
    template_name = "core/admissions_info.html"


class CharityWingView(TemplateView):
    template_name = "core/charity.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"


class CareerView(TemplateView):
    template_name = "core/career.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_openings"] = JobOpening.objects.filter(is_active=True)
        return context


class DashboardRouterView(RedirectView):
    """Redirects logged-in users to the appropriate role dashboard."""

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user: User = self.request.user
        if not user.is_authenticated:
            return reverse_lazy("login")

        if user.is_admin():
            return reverse_lazy("core:admin_dashboard")
        if user.is_staff_member():
            return reverse_lazy("core:staff_dashboard")
        if user.is_student():
            return reverse_lazy("core:student_dashboard")
        if user.is_parent():
            return reverse_lazy("core:parent_dashboard")
        if user.is_sponsor():
            return reverse_lazy("core:sponsor_dashboard")
        if user.is_committee_member():
            return reverse_lazy("core:committee_dashboard")
        if user.is_applicant():
            return reverse_lazy("admissions:dashboard")

        return reverse_lazy("core:home")


class BaseDashboardView(RoleRequiredMixin, TemplateView):
    """Base template for all dashboards; restricts by role."""

    allowed_roles: list[str] = []
    template_name = "core/dashboard_base.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AdminDashboardView(BaseDashboardView):
    template_name = "core/dashboard_admin.html"
    allowed_roles = [User.Roles.ADMIN]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Admin dashboard statistics
        context.update({
            'total_students': StudentProfile.objects.count(),
            'total_staff': StaffProfile.objects.count(),
            'pending_applications': AdmissionApplication.objects.filter(status=AdmissionApplication.Status.UNDER_REVIEW).count(),
            'total_applications': AdmissionApplication.objects.count(),
            'total_payments': Payment.objects.filter(status=Payment.Status.SUCCESS).count(),
            'total_revenue': Payment.objects.filter(status=Payment.Status.SUCCESS).aggregate(
                total=models.Sum('amount')
            )['total'] or 0,
            'active_sponsorships': SponsorshipAllocation.objects.filter(active=True).count(),
        })
        return context


class StaffDashboardView(BaseDashboardView):
    template_name = "core/dashboard_staff.html"
    allowed_roles = [User.Roles.STAFF, User.Roles.ADMIN]


class StudentDashboardView(BaseDashboardView):
    template_name = "core/dashboard_student.html"
    allowed_roles = [User.Roles.STUDENT, User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch Student Profile (Enrolled Course)
        try:
            context['student_profile'] = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            context['student_profile'] = None

        # Fetch Admission Applications
        context['applications'] = AdmissionApplication.objects.filter(user=self.request.user).order_by('-submitted_at')
        return context


class ParentDashboardView(BaseDashboardView):
    template_name = "core/dashboard_parent.html"
    allowed_roles = [User.Roles.PARENT, User.Roles.ADMIN]


class SponsorDashboardView(BaseDashboardView):
    template_name = "core/dashboard_sponsor.html"
    allowed_roles = [User.Roles.SPONSOR, User.Roles.ADMIN]


class CommitteeDashboardView(BaseDashboardView):
    template_name = "core/dashboard_committee.html"
    allowed_roles = [User.Roles.COMMITTEE, User.Roles.ADMIN]

# --- Academic Year Management ---
class AcademicYearListView(RoleRequiredMixin, ListView):
    model = AcademicYear
    template_name = "core/academicyear_list.html"
    context_object_name = 'academic_years'
    allowed_roles = [User.Roles.ADMIN]

class AcademicYearCreateView(RoleRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('core:academicyear_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Add Academic Year"
        return context

class AcademicYearUpdateView(RoleRequiredMixin, UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('core:academicyear_list')
    allowed_roles = [User.Roles.ADMIN]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Update Academic Year"
        return context


# --- Institution Management ---
class InstitutionManagementListView(RoleRequiredMixin, ListView):
    model = Institution
    template_name = "core/institution_list_admin.html"
    context_object_name = 'institutions'
    allowed_roles = [User.Roles.ADMIN]


class InstitutionCreateView(RoleRequiredMixin, CreateView):
    model = Institution
    form_class = InstitutionForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('core:institution_manage')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Add Institution"
        return context


class InstitutionUpdateView(RoleRequiredMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('core:institution_manage')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Update Institution"
        return context


# --- Job Application Management ---
class JobApplicationCreateView(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = "core/job_application_form.html"
    success_url = reverse_lazy('core:job_application_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        context['job'] = JobOpening.objects.get(pk=job_id)
        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        form.instance.job = JobOpening.objects.get(pk=job_id)
        return super().form_valid(form)


class JobApplicationListView(RoleRequiredMixin, ListView):
    model = JobApplication
    template_name = "core/job_application_list.html"
    context_object_name = 'applications'
    allowed_roles = [User.Roles.ADMIN]


class JobApplicationUpdateView(RoleRequiredMixin, UpdateView):
    model = JobApplication
    fields = ['status']
    template_name = "core/job_application_review.html"
    success_url = reverse_lazy('core:job_application_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Review Application: {self.object.full_name}"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Application status updated to {self.object.get_status_display()}.")
        return super().form_valid(form)


class JobApplicationSuccessView(TemplateView):
    template_name = "core/job_application_success.html"


import subprocess
class UpdateHistoryView(RoleRequiredMixin, TemplateView):
    template_name = "core/update_history.html"
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # git log --pretty=format:"%h|%an|%ar|%s" -n 20
            result = subprocess.check_output(
                ['git', 'log', '--pretty=format:%H|%an|%ad|%s', '--date=short', '-n', '20'],
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            
            commits = []
            for line in result.split('\n'):
                if line.strip():
                    parts = line.split('|', 3)
                    if len(parts) == 4:
                        message = parts[3]
                        
                        # Filtering: Skip technical commits
                        lower_msg = message.lower()
                        if any(x in lower_msg for x in ['merge branch', 'merge remote', 'chore:', 'refactor:', 'style:', 'test:']):
                            continue
                            
                        # Formatting: Make prefixes user-friendly
                        prefix_map = {
                            'feat:': 'New Feature:',
                            'fix:': 'Bug Fix:',
                            'docs:': 'Documentation:',
                            'perf:': 'Performance:',
                            'ui:': 'UI Update:'
                        }
                        
                        for prefix, replacement in prefix_map.items():
                            if message.lower().startswith(prefix):
                                message = replacement + message[len(prefix):]
                                break
                        
                        commits.append({
                            'hash': parts[0],
                            'short_hash': parts[0][:7],
                            'author': parts[1],
                            'date': parts[2],
                            'message': message
                        })
            context['commits'] = commits
        except Exception as e:
            context['error'] = f"Could not retrieve update history: {str(e)}"
            context['commits'] = []
            
        context['page_title'] = "Update History"
        return context
