from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import User

class CustomLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

from .forms import ApplicantSignUpForm
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = ApplicantSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Create Account")
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Account created successfully. Please login."))
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone', 'organization_name']
    template_name = "core/generic_form.html"
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("My Profile")
        context['page_icon'] = "bi-person-circle"
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Profile updated successfully."))
        return super().form_valid(form)
