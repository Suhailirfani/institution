from django import forms
from .models import AcademicYear, Institution, JobApplication

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'code', 'address', 'phone', 'email', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us why you are a good fit...'}),
            'resume': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }
