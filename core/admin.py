from django.contrib import admin
from .models import (
    AcademicYear, Institution, CMSPage, NotificationLog, NewsItem, JobOpening
)

# Register your models here.

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')

@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('to', 'subject', 'channel', 'created_at')
    list_filter = ('channel', 'created_at')
    search_fields = ('to', 'subject', 'body')
    readonly_fields = ('to', 'subject', 'body', 'channel', 'meta', 'created_at')

    def has_add_permission(self, request):
        return False

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
