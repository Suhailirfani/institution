from django.contrib import admin
from .models import AdmissionApplication, Programme

# Register your models here.

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'institution', 'is_active')
    list_filter = ('institution', 'is_active')
    search_fields = ('name', 'code')

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'programme', 'status', 'submitted_at')
    list_filter = ('status', 'programme', 'submitted_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('submitted_at', 'reviewed_at', 'reviewed_by')
    fieldsets = (
        ('Applicant Details', {
            'fields': ('full_name', 'date_of_birth', 'email', 'phone', 'address')
        }),
        ('Academic Info', {
            'fields': ('academic_year', 'programme')
        }),
        ('Guardian Info', {
            'fields': ('guardian_name', 'guardian_phone')
        }),
        ('Status', {
            'fields': ('status', 'remarks', 'reviewed_by', 'reviewed_at')
        })
    )
