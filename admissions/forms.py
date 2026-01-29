from django import forms
from .models import AdmissionApplication, AdmissionDocument

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'academic_year', 'programme', 'full_name', 'date_of_birth',
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
