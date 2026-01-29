from django.urls import path

app_name = "payments"

from . import views

app_name = "payments"

urlpatterns = [
    path("list/", views.PaymentListView.as_view(), name="payment_list"),
]



