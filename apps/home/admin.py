# apps/home/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Module
from apps.organization.models import Department, Role, UserRole  # Import other models
from authentication.models import CustomUser  # Import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add or modify fieldsets to include custom fields in the admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('pj_number', 'phone', 'mobile', 'departments',)}), #Added the many to many field
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('pj_number', 'phone', 'mobile','departments',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'get_departments') #added get_departments
    search_fields = ('username', 'email', 'first_name', 'last_name', 'pj_number')
    list_filter = ('is_staff', 'is_superuser', 'departments')

    def get_departments(self, obj): # added a function to return the department of a user
        return ", ".join([d.name for d in obj.departments.all()])
    get_departments.short_description = 'Departments'

admin.site.register(CustomUser, CustomUserAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

admin.site.register(Department, DepartmentAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'job_group', 'is_active')
    search_fields = ('title', 'department__name', 'job_group')
    list_filter = ('department', 'job_group', 'is_active')
    filter_horizontal = ('permissions',)  # Use filter_horizontal for ManyToMany

admin.site.register(Role, RoleAdmin)

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_at', 'is_active')
    search_fields = ('user__username', 'role__title', 'role__department__name')
    list_filter = ('role__department', 'role', 'is_active')
    raw_id_fields = ('user', 'role')  # Use raw_id_fields for better performance with many users/roles

admin.site.register(UserRole, UserRoleAdmin)


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'display_departments', 'icon_class', 'url_name')  # Keep display_departments
    search_fields = ('name', 'description', 'url_name')
    list_filter = ('departments',)  # Keep list_filter
    filter_horizontal = ('departments',) # Add filter_horizontal

    def display_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()])
    display_departments.short_description = 'Departments'

admin.site.register(Module, ModuleAdmin)