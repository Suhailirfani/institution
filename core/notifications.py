from django.conf import settings
from django.core.mail import send_mail

from .models import NotificationLog


def send_email_notification(subject: str, body: str, to_email: str, meta: dict | None = None) -> None:
    """MVP email notification wrapper that also logs to the database."""
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=True,
    )
    NotificationLog.objects.create(
        channel=NotificationLog.EMAIL,
        to=to_email,
        subject=subject,
        body=body,
        meta=meta or {},
    )


def send_sms_notification(message: str, to_phone: str, meta: dict | None = None) -> None:
    """Placeholder SMS notification function.

    Integrate with an SMS provider by using settings.SMS_GATEWAY_API_URL / API_KEY.
    """
    # TODO: Call external SMS API here in production.
    NotificationLog.objects.create(
        channel=NotificationLog.SMS,
        to=to_phone,
        subject="",
        body=message,
        meta=meta or {},
    )



