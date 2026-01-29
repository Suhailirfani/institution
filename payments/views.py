from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from core.views import RoleRequiredMixin
from .models import Payment

class PaymentListView(RoleRequiredMixin, ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = 'payments'
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Payments")
        context['page_icon'] = "bi-credit-card"
        return context
