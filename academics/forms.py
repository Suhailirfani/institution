from django import forms
from accounts.models import User
from .models import ClassRoom, StudentProfile, StaffProfile, Subject

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['institution', 'academic_year', 'standard', 'division']

class StudentProfileForm(forms.ModelForm):
    # Including user fields could be complex here, so keeping it simple for MVP
    # Ideally, we would use a formset or a custom form to handle both User and Profile
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = StudentProfile
        fields = ['admission_number', 'date_of_birth', 'classroom']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        student_profile = super().save(commit=False)
        # In a real app, we'd handle user creation more robustly
        # For MVP, we might assume the User exists or created separately, 
        # but to make this form useful, let's just save the profile if user is set.
        if commit:
            student_profile.save()
        return student_profile


class StaffCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = StaffProfile
        fields = ['department', 'designation', 'joining_date', 'qualification']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        from django.db import transaction
        
        # We need to save both User and Profile
        if not commit:
            raise NotImplementedError("StaffCreationForm does not support save(commit=False)")

        with transaction.atomic():
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=User.Roles.STAFF
            )
            
            staff_profile = super().save(commit=False)
            staff_profile.user = user
            staff_profile.save()
            
        return staff_profile
