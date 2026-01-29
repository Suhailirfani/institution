from django.conf import settings
from .models import NotificationLog

class NotificationService:
    """Service to handle sending notifications via SMS or Email."""

    @staticmethod
    def send_sms(to_number: str, message: str, meta: dict = None):
        """
        Send an SMS to the given number.
        For MVP, this logs to the database and console.
        """
        # In a real app, integrate Twilio/AWS SNS/local gateway here.
        # e.g., requests.post(settings.SMS_GATEWAY_URL, ...)
        
        print(f"[{settings.TIME_ZONE}] SMS to {to_number}: {message}")
        
        NotificationLog.objects.create(
            channel=NotificationLog.SMS,
            to=to_number,
            body=message,
            meta=meta or {}
        )

    @staticmethod
    def send_email(to_email: str, subject: str, message: str, meta: dict = None):
        """
        Send an email.
        """
        # Use Django's send_mail
        from django.core.mail import send_mail
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            # Log successful attempt
            NotificationLog.objects.create(
                channel=NotificationLog.EMAIL,
                to=to_email,
                subject=subject,
                body=message,
                meta=meta or {"status": "sent"}
            )
        except Exception as e:
            # Log failure
            print(f"Failed to send email to {to_email}: {e}")
            NotificationLog.objects.create(
                channel=NotificationLog.EMAIL,
                to=to_email,
                subject=subject,
                body=f"FAILED: {message}",
                meta=meta or {"error": str(e)}
            )

    @classmethod
    def send_attendance_alert(cls, student, date, status):
        """
        Send an alert to the parent regarding student attendance.
        """
        if status == 'A': # Absent
            # Find parent phone
            # Assuming student.parents.first() gets the primary guardian
            parent = student.parents.first()
            if parent and parent.user.phone:
                message = (
                    f"Alert: Your ward {student.user.get_full_name()} "
                    f"was marked ABSENT on {date}. "
                    f"Please contact the admin if this is an error."
                )
                cls.send_sms(
                    to_number=parent.user.phone, 
                    message=message,
                    meta={"student_id": student.id, "type": "attendance_alert"}
                )
