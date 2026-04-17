from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from core.views import RoleRequiredMixin
from .models import Payment, Donation
from .services import create_donation_razorpay_order, verify_razorpay_signature

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


class DonateView(View):
    def get(self, request):
        categories = Donation.Category.choices
        return render(request, "payments/donate.html", {
            "categories": categories,
            "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID
        })

    def post(self, request):
        donor_name = request.POST.get('donor_name')
        donor_email = request.POST.get('donor_email')
        donor_phone = request.POST.get('donor_phone')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        
        # basic validation
        if not all([donor_name, amount, category]):
            return render(request, "payments/donate.html", {
                "categories": Donation.Category.choices,
                "error": "Name, Category and Amount are required",
                "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID
            })
            
        donation = Donation.objects.create(
            donor_name=donor_name,
            donor_email=donor_email,
            donor_phone=donor_phone,
            category=category,
            amount=amount,
            currency="INR"
        )
        
        order = create_donation_razorpay_order(donation)
        
        return render(request, "payments/donate_checkout.html", {
            "donation": donation,
            "order": order,
            "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,
        })

@method_decorator(csrf_exempt, name='dispatch')
class DonationCallbackView(View):
    def post(self, request):
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        if not verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
            try:
                donation = Donation.objects.get(razorpay_order_id=razorpay_order_id)
                donation.status = Donation.Status.FAILED
                donation.save()
            except Donation.DoesNotExist:
                pass
            return render(request, "payments/donation_failed.html")
            
        try:
            donation = Donation.objects.get(razorpay_order_id=razorpay_order_id)
            donation.status = Donation.Status.SUCCESS
            donation.razorpay_payment_id = razorpay_payment_id
            donation.razorpay_signature = razorpay_signature
            donation.save()
            return render(request, "payments/donation_success.html", {"donation": donation})
        except Donation.DoesNotExist:
            return render(request, "payments/donation_failed.html")
