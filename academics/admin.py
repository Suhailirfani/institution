from django.contrib import admin
from .models import (
    ClassRoom, Subject, StaffProfile, StudentProfile, ParentProfile, 
    AttendanceRecord, Exam, ExamResult
)

# Register your models here.

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('standard', 'division', 'institution', 'academic_year')
    list_filter = ('institution', 'academic_year')
    search_fields = ('standard', 'division')
    inlines = [SubjectInline]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'classroom')
    list_filter = ('classroom__institution', 'classroom__academic_year')
    search_fields = ('name', 'code')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'institution', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'designation')
    list_filter = ('institution',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'classroom', 'date_of_birth')
    search_fields = ('admission_number', 'user__first_name', 'user__last_name', 'user__username')
    list_filter = ('classroom__institution', 'classroom__academic_year', 'classroom')

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__first_name', 'user__username')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'marked_by')
    list_filter = ('date', 'status', 'student__classroom')
    search_fields = ('student__user__first_name', 'student__admission_number')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom', 'date', 'academic_year')
    list_filter = ('classroom', 'academic_year')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'subject', 'marks_obtained', 'grade')
    list_filter = ('exam', 'subject')
    search_fields = ('student__user__first_name',)
