from django.urls import path

app_name = "payments"

from . import views

app_name = "payments"

urlpatterns = [
    path("list/", views.PaymentListView.as_view(), name="payment_list"),
    path("donate/", views.DonateView.as_view(), name="donate"),
    path("donate/callback/", views.DonationCallbackView.as_view(), name="donate_callback"),
]



