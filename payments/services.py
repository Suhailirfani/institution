from decimal import Decimal
from typing import Any

import razorpay
from django.conf import settings

from .models import Payment


def get_razorpay_client() -> razorpay.Client:
    """Create a Razorpay client using configured credentials."""
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def create_razorpay_order(payment: Payment) -> dict[str, Any]:
    """Create a Razorpay order for a Payment instance (amount in paise)."""
    client = get_razorpay_client()
    amount_paise = int(Decimal(payment.amount) * 100)
    order = client.order.create(
        {
            "amount": amount_paise,
            "currency": payment.currency,
            "receipt": f"pay_{payment.pk}",
            "payment_capture": 1,
        }
    )
    payment.razorpay_order_id = order.get("id", "")
    payment.save(update_fields=["razorpay_order_id"])
    return order


def verify_razorpay_signature(
    razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str
) -> bool:
    """Verify the Razorpay payment signature."""
    client = get_razorpay_client()
    try:
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )
    except razorpay.errors.SignatureVerificationError:
        return False
    return True



