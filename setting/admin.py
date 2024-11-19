from django.contrib import admin
from .models import SiteSettings, Job

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'location', 'created_at', 'updated_at']
    search_fields = ['email', 'phone']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'job_type', 'created_at']
    search_fields = ['name', 'location']