from django.db import models


class Lesson(models.Model):
    DIFFICULTY_CHOICES = [
        ('1', 'Beginner'),
        ('2', 'Intermediate'),
        ('3', 'Advanced'),
    ]
    topic = models.CharField(max_length=100)       # e.g. "Introduction to Python"
    subtopic = models.CharField(max_length=100)    # e.g. "Variables"
    code_example = models.TextField()              # Python code snippet
    code_explanation = models.TextField()          # "What this code does"
    difficulty_level = models.CharField(
        max_length=50,
        choices=DIFFICULTY_CHOICES,
        default='1',
        help_text="The difficulty level of the lesson."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["topic", "subtopic"]

    def __str__(self):
        return f"{self.topic} - {self.subtopic}"


class LessonTranslation(models.Model):
    LANG_CHOICES = [
        ("en", "English"),
        ("yo", "Yoruba"),
        ("ig", "Igbo"),
        ("ha", "Hausa"),
    ]

    lesson = models.ForeignKey(Lesson, related_name="translations", on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANG_CHOICES)
    concept_text = models.TextField()              # Explanation in native language
    audio_file = models.FileField(upload_to="audio/", blank=True, null=True)

    class Meta:
        unique_together = ("lesson", "language")

    def __str__(self):
        return f"{self.lesson.subtopic} ({self.get_language_display()})"
