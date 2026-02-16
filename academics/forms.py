from django import forms
from accounts.models import User
from .models import ClassRoom, StudentProfile, StaffProfile, Subject, Exam, ExamResult

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
        fields = ['admission_number', 'whatsapp_number', 'date_of_birth', 'classroom', 'father_name', 'mother_name', 'address', 'blood_group']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
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
        fields = ['mobile_number', 'place', 'address', 'department', 'designation', 'joining_date', 'qualification']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Contact Number'}),
            'place': forms.TextInput(attrs={'placeholder': 'City/Town'}),
        }

    def save(self, commit=True):
        from django.db import transaction
        
        # We need to save both User and Profile
        if not commit:
            raise NotImplementedError("StaffCreationForm does not support save(commit=False)")

        with transaction.atomic():
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=User.Roles.STAFF
            )
            
            staff_profile = super().save(commit=False)
            staff_profile.user = user

            # Assign to default institution (first active one)
            from core.models import Institution
            staff_profile.institution = Institution.objects.filter(is_active=True).first() or Institution.objects.first()

            staff_profile.save()
            
            
        return staff_profile


class StaffUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = StaffProfile
        fields = ['mobile_number', 'place', 'address', 'department', 'designation', 'joining_date', 'qualification']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        staff_profile = super().save(commit=False)
        
        user = staff_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        if commit:
            staff_profile.save()
        return staff_profile


class StaffBulkImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload Excel File",
        help_text="Upload .xlsx file with columns: First Name, Last Name, Email, Mobile, Place, Department, Designation, Qualification"
    )


class StudentCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = StudentProfile
        fields = ['admission_number', 'whatsapp_number', 'date_of_birth', 'classroom', 'father_name', 'mother_name', 'address', 'blood_group']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'whatsapp_number': forms.TextInput(attrs={'placeholder': 'e.g. 9876543210'}),
        }

    def save(self, commit=True):
        from django.db import transaction
        
        if not commit:
            raise NotImplementedError("StudentCreationForm does not support save(commit=False)")

        with transaction.atomic():
            user = User.objects.create_user(
                username=self.cleaned_data['email'], # Use email as username default
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=User.Roles.STUDENT
            )
            
            student_profile = super().save(commit=False)
            student_profile.user = user
            student_profile.save()
            
        return student_profile


class StudentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = StudentProfile
        fields = ['admission_number', 'whatsapp_number', 'date_of_birth', 'classroom', 'father_name', 'mother_name', 'address', 'blood_group']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'whatsapp_number': forms.TextInput(attrs={'placeholder': 'e.g. 9876543210'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        student_profile = super().save(commit=False)
        
        user = student_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        if commit:
            student_profile.save()
        return student_profile


class StudentBulkImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload Excel File",
        help_text="Upload .xlsx file with columns: First Name, Last Name, Email, DOB, Admin No, WhatsApp, Class Code, Father Name, Mother Name, Address, Blood Group"
    )


# --- Result Management Forms ---

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'classroom', 'max_marks', 'pass_marks']
        widgets = {
             # classroom is typically handled in view context or hidden
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'academic_year', 'classroom', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['student', 'subject', 'marks_obtained', 'max_marks']
        
    def clean(self):
        cleaned_data = super().clean()
        marks = cleaned_data.get('marks_obtained')
        max_marks = cleaned_data.get('max_marks')
        
        if marks and max_marks and marks > max_marks:
            self.add_error('marks_obtained', "Marks obtained cannot exceed maximum marks.")
        return cleaned_data

class BulkExamResultForm(forms.Form):
    """
    Form for entering marks for a single student in a bulk entry view.
    Designed to be used in a formset.
    """
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    student_name = forms.CharField(disabled=True, required=False)
    marks_obtained = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, required=False)
    is_absent = forms.BooleanField(required=False, label="Absent")

    def clean(self):
        cleaned_data = super().clean()
        marks = cleaned_data.get('marks_obtained')
        is_absent = cleaned_data.get('is_absent')

        if not is_absent and marks is None:
             # It's okay to have empty marks (not entered yet), but if absent is false and marks are valid...
             # Actually, let's allow empty to mean "not entered".
             pass
        return cleaned_data
