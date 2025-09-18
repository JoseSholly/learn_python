from django.contrib import admin
from .models import Lesson, LessonTranslation

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('topic', 'subtopic', 'difficulty_level', 'created_at')
    list_filter = ('difficulty_level', 'created_at')
    search_fields = ('topic', 'subtopic', 'code_example', 'code_explanation')
    ordering = ('topic', 'subtopic')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('topic', 'subtopic', 'difficulty_level')
        }),
        ('Content', {
            'fields': ('code_example', 'code_explanation')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

@admin.register(LessonTranslation)
class LessonTranslationAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'language', 'has_audio')
    list_filter = ('language',)
    search_fields = ('lesson__topic', 'lesson__subtopic', 'concept_text')
    autocomplete_fields = ('lesson',)
    
    def has_audio(self, obj):
        return bool(obj.audio)
    has_audio.boolean = True
    has_audio.short_description = 'Audio Available'

    fieldsets = (
        (None, {
            'fields': ('lesson', 'language')
        }),
        ('Content', {
            'fields': ('concept_text', 'audio')
        }),
    )