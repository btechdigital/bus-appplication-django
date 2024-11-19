from django.contrib import admin
from .models import Driver, Service
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'profession', 'created_at']
    search_fields = ['name', 'profession']

@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):
    list_display = ['title', 'slug', 'created_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}  # Auto-populate slug based on title
    summernote_fields = ('description',)
