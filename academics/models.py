from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AcademicYear, Institution


class ClassRoom(models.Model):
    """Represents a class/division for a given academic year."""

    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="classrooms",
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="classrooms",
    )
    standard = models.CharField(
        max_length=50,
        help_text=_("e.g. Grade 1, BA Arabic, etc."),
    )
    division = models.CharField(max_length=10, blank=True, help_text=_("e.g. A, B"))

    class Meta:
        unique_together = ("institution", "academic_year", "standard", "division")
        verbose_name = _("Class Room")
        verbose_name_plural = _("Class Rooms")

    def __str__(self) -> str:
        div = f" - {self.division}" if self.division else ""
        return f"{self.standard}{div} ({self.academic_year})"


class Subject(models.Model):
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    pass_marks = models.DecimalField(max_digits=5, decimal_places=2, default=40.00)

    class Meta:
        unique_together = ("classroom", "code")

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class StaffProfile(models.Model):
    """Profile for staff users."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    designation = models.CharField(max_length=255, blank=True)
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="staff_members",
    )
    department = models.CharField(max_length=255, blank=True)
    qualification = models.CharField(max_length=255, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, help_text=_("Contact Number"), default="")
    place = models.CharField(max_length=100, help_text=_("City/Town/Village"), default="")
    address = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username}"


class StudentProfile(models.Model):
    """Profile for students linked to a user account."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    admission_number = models.CharField(max_length=50, unique=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text=_("Active WhatsApp number"))
    date_of_birth = models.DateField()
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.PROTECT,
        related_name="students",
    )
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(
        max_length=5, 
        blank=True, 
        choices=[
            ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
        ]
    )

    def __str__(self) -> str:
        return f"{self.admission_number} - {self.user.get_full_name() or self.user.username}"


class ParentProfile(models.Model):
    """Profile for parents/guardians."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_profile",
    )
    students = models.ManyToManyField(
        StudentProfile,
        related_name="parents",
        blank=True,
    )

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username


class AttendanceRecord(models.Model):
    """Daily attendance record for a student."""

    class Status(models.TextChoices):
        PRESENT = "P", _("Present")
        ABSENT = "A", _("Absent")
        LEAVE = "L", _("On Leave")

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    date = models.DateField()
    status = models.CharField(max_length=1, choices=Status.choices)
    marked_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        related_name="marked_attendance",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.student} - {self.date} - {self.get_status_display()}"


class Exam(models.Model):
    """Represents an exam for a class."""

    name = models.CharField(max_length=255)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name} - {self.classroom}"


class ExamResult(models.Model):
    """Marks for a student in a given exam and subject."""

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="results",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="exam_results",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="exam_results",
    )
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=10, blank=True)

    class Meta:
        unique_together = ("exam", "student", "subject")

    def __str__(self) -> str:
        return f"{self.exam} - {self.student} - {self.subject}"
