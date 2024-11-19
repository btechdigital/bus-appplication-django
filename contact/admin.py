from django.contrib import admin
from .models import ContactForm, FAQs

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'name', 'email', 'phone', 'created_at')
    search_fields = ('subject', 'name', 'email', 'phone')

class FAQsAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)

admin.site.register(ContactForm, ContactFormAdmin)
admin.site.register(FAQs, FAQsAdmin)