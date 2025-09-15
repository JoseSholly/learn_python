from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProgress


# Custom admin for the User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ("email", "is_verified", "is_staff", "is_active", "date_joined")
    # Fields to filter by in the admin
    list_filter = ("is_verified", "is_staff", "is_active")
    # Fields to search
    search_fields = ("email",)
    # Fields to edit in the detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # Fields for adding a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_verified"),
            },
        ),
    )
    # Ordering in the list view
    ordering = ("email",)
    # Remove username from filter since it's not used
    filter_horizontal = ()


# Custom admin for the UserProgress model
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("user", "lesson", "completed", "completed_at")
    # Fields to filter by in the admin
    list_filter = ("completed", "user", "lesson")
    # Fields to search
    search_fields = ("user__email", "lesson__subtopic")
    # Fields to edit in the detail view
    fieldsets = (
        (None, {"fields": ("user", "lesson", "completed", "completed_at")}),
    )
    # Ordering in the list view
    ordering = ("user", "lesson")
    # Read-only fields to prevent accidental changes
    readonly_fields = ("completed_at",)

    def get_queryset(self, request):
        # Optimize queries by selecting related objects
        return super().get_queryset(request).select_related("user", "lesson")