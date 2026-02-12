from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ApplicantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.APPLICANT
        if commit:
            user.save()
        return user
