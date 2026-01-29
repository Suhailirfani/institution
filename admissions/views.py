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

class AdmissionApplicationCreateView(CreateView):
    model = AdmissionApplication
    form_class = AdmissionApplicationForm
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('core:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Apply for Admission")
        context['page_icon'] = "bi-mortarboard"
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Application submitted successfully! We will contact you soon."))
        return super().form_valid(form)

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

class AdmissionApplicationDetailView(RoleRequiredMixin, UpdateView):
    model = AdmissionApplication
    form_class = AdmissionReviewForm
    template_name = "core/generic_form.html"
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
        form.instance.reviewed_at = form.instance.updated_at # or now()
        messages.success(self.request, _("Application status updated."))
        return super().form_valid(form)
