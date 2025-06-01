from django.contrib import admin
from .models import PersonalInfo, Skill, Experience, Project, ProjectImage, ContactMessage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'title', 'email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency_level', 'is_featured', 'order']
    list_filter = ['category', 'proficiency_level', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_featured']
    ordering = ['category', 'order', 'name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['is_current', 'start_date', 'company']
    search_fields = ['position', 'company', 'description']
    list_editable = ['order']
    filter_horizontal = ['technologies']
    ordering = ['-start_date', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date', 'is_featured', 'order']
    list_filter = ['status', 'is_featured', 'start_date', 'technologies']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_featured']
    filter_horizontal = ['technologies']
    inlines = [ProjectImageInline]
    ordering = ['-is_featured', 'order', '-start_date']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
