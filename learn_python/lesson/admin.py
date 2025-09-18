from django.contrib import admin
from .models import Lesson, LessonTranslation


# Inline admin for LessonTranslation
class LessonTranslationInline(admin.TabularInline):
    model = LessonTranslation
    extra = 1  # Number of empty forms to display
    fields = ("language", "concept_text", "audio")
    readonly_fields = ("audio",)  # Make audio read-only to prevent accidental changes


# Custom admin for the Lesson model
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'subtopic', 'difficulty_level', 'created_at')
    list_filter = ('difficulty_level', 'created_at')
    search_fields = ('topic', 'subtopic', 'code_explanation')
    ordering = ('difficulty_level', )
    fieldsets = (
        (None, {
            'fields': ('topic', 'subtopic', 'difficulty_level')
        }),
        ('Code Details', {
            'fields': ('code_example', 'code_explanation')
        }),
    )


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
        (None, {"fields": ("lesson", "language", "concept_text", "audio")}),
    )
    # Ordering in the list view
    ordering = ("lesson", "language")
    # Read-only fields
    # readonly_fields = ("audio",)

    def get_queryset(self, request):
        # Optimize queries by selecting related objects
        return super().get_queryset(request).select_related("lesson")