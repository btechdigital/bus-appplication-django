from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Tag


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'user', 'created_at', 'category')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('user', 'category', 'tags', 'created_at')  # Fields to filter by
    search_fields = ('title', 'content')  # Search fields
    summernote_fields = ('content',)  # Use Summernote for content field


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display in list view
    search_fields = ('name',)  # Search fields


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Fields to display in list view
    search_fields = ('name',)  # Search fields



admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)