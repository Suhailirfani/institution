from django import forms
from .models import AdmissionApplication, AdmissionDocument

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'institution', 'academic_year', 'programme', 'full_name', 'date_of_birth',
            'email', 'phone', 'address', 'guardian_name', 'guardian_phone'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class AdmissionReviewForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

from academics.models import StudentProfile
class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['admission_number', 'classroom', 'date_of_birth', 'father_name', 'mother_name', 'address', 'blood_group']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].queryset = self.fields['classroom'].queryset.select_related('academic_year')

from .models import Programme
class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ['institution', 'name', 'code', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
