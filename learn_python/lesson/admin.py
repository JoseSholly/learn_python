from django.contrib import admin
from .models import Lesson, LessonTranslation


# Inline admin for LessonTranslation
class LessonTranslationInline(admin.TabularInline):
    model = LessonTranslation
    extra = 1  # Number of empty forms to display
    fields = ("language", "concept_text", "audio_file")
    readonly_fields = ("audio_file",)  # Make audio_file read-only to prevent accidental changes


# Custom admin for the Lesson model
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("topic", "subtopic", "created_at")
    # Fields to filter by in the admin
    list_filter = ("topic", "created_at")
    # Fields to search
    search_fields = ("topic", "subtopic", "code_example", "code_explanation")
    # Fields to edit in the detail view
    fieldsets = (
        (None, {"fields": ("topic", "subtopic")}),
        ("Content", {"fields": ("code_example", "code_explanation")}),
        ("Metadata", {"fields": ("created_at",)}),
    )
    # Inline editing for translations
    inlines = [LessonTranslationInline]
    # Ordering in the list view
    ordering = ("topic", "subtopic")
    # Read-only fields
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        # Optimize queries
        return super().get_queryset(request)


# Custom admin for the LessonTranslation model
@admin.register(LessonTranslation)
class LessonTranslationAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("lesson", "language", "get_language_display", "concept_text")
    # Fields to filter by in the admin
    list_filter = ("language", "lesson")
    # Fields to search
    search_fields = ("lesson__subtopic", "lesson__topic", "concept_text")
    # Fields to edit in the detail view
    fieldsets = (
        (None, {"fields": ("lesson", "language", "concept_text", "audio_file")}),
    )
    # Ordering in the list view
    ordering = ("lesson", "language")
    # Read-only fields
    readonly_fields = ("audio_file",)

    def get_queryset(self, request):
        # Optimize queries by selecting related objects
        return super().get_queryset(request).select_related("lesson")