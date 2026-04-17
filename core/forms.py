from django import forms
from .models import AcademicYear, Institution, JobApplication, CharityApplication, NewsItem


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


class CharityApplicationForm(forms.ModelForm):
    class Meta:
        model = CharityApplication
        fields = ['full_name', 'phone', 'category', 'description', 'document']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'News headline...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional longer description or detail...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }