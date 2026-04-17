from decimal import Decimal
from typing import Any
from django.conf import settings
from .models import Payment

# import razorpay  # Revoked for now

def get_razorpay_client() -> Any:
    """Mock Razorpay client."""
    return None

def create_donation_razorpay_order(donation: 'Donation') -> dict[str, Any]:
    """Mock Razorpay order for a Donation."""
    donation.razorpay_order_id = f"mock_don_{donation.pk}"
    donation.save(update_fields=["razorpay_order_id"])
    return {"id": donation.razorpay_order_id, "amount": int(Decimal(donation.amount) * 100), "currency": "INR"}

def create_razorpay_order(payment: Payment) -> dict[str, Any]:
    """Mock Razorpay order for a Payment."""
    payment.razorpay_order_id = f"mock_pay_{payment.pk}"
    payment.save(update_fields=["razorpay_order_id"])
    return {"id": payment.razorpay_order_id, "amount": int(Decimal(payment.amount) * 100), "currency": "INR"}

def verify_razorpay_signature(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
    """Always return True for mock offline dev integration."""
    return True
