from django.db import models
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from accounts.models import User
from accounts.permissions import RoleRequiredMixin
from admissions.models import AdmissionApplication
from academics.models import StudentProfile, StaffProfile
from payments.models import Payment
from sponsorship.models import SponsorshipAllocation
from .models import NewsItem, JobOpening


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


class ParentDashboardView(BaseDashboardView):
    template_name = "core/dashboard_parent.html"
    allowed_roles = [User.Roles.PARENT, User.Roles.ADMIN]


class SponsorDashboardView(BaseDashboardView):
    template_name = "core/dashboard_sponsor.html"
    allowed_roles = [User.Roles.SPONSOR, User.Roles.ADMIN]


class CommitteeDashboardView(BaseDashboardView):
    template_name = "core/dashboard_committee.html"
    allowed_roles = [User.Roles.COMMITTEE, User.Roles.ADMIN]
