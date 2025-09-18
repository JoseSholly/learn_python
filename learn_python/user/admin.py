from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProgress

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_verified'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at')
    search_fields = ('user__email', 'lesson__topic', 'lesson__subtopic')
    autocomplete_fields = ('user', 'lesson')
    readonly_fields = ('completed_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'lesson', 'completed')
        }),
        ('Metadata', {
            'fields': ('completed_at',)
        }),
    )