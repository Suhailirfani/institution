from django.db.models import QuerySet
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, DetailView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from .models import User
from .permissions import RoleRequiredMixin
from .forms import ApplicantSignUpForm, UserAdminCreationForm, UserAdminUpdateForm

class CustomLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

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

# --- User Management CRUD ---

class UserListView(RoleRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    allowed_roles = [User.Roles.ADMIN]
    paginate_by = 25

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        role = self.request.GET.get('role')
        search = self.request.GET.get('search')
        if role:
            qs = qs.filter(role=role)
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(first_name__icontains=search) | qs.filter(last_name__icontains=search)
        return qs.order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("User Management")
        context['roles'] = User.Roles.choices
        return context

class UserCreateView(RoleRequiredMixin, CreateView):
    model = User
    form_class = UserAdminCreationForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy('accounts:user_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Add New User")
        return context

    def form_valid(self, form):
        messages.success(self.request, _("User created successfully."))
        return super().form_valid(form)

class UserUpdateView(RoleRequiredMixin, UpdateView):
    model = User
    form_class = UserAdminUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy('accounts:user_list')
    allowed_roles = [User.Roles.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update User")
        context['object'] = self.object
        return context

    def form_valid(self, form):
        messages.success(self.request, _("User details updated successfully."))
        return super().form_valid(form)

class UserSoftDeleteView(RoleRequiredMixin, DetailView):
    model = User
    allowed_roles = [User.Roles.ADMIN]

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            messages.error(request, _("You cannot deactivate yourself!"))
        else:
            user.is_active = not user.is_active
            user.save()
            status = "activated" if user.is_active else "deactivated"
            messages.success(request, f"User {user.username} has been {status}.")
        return redirect('accounts:user_list')
