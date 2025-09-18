import os
from django.core.management.base import BaseCommand
from lesson.models import Lesson, LessonTranslation
from spitch import Spitch


class Command(BaseCommand):
    help = "Translate Lesson explanations into Yoruba, Igbo, Hausa using Spitch API (no audio)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--languages",
            nargs="+",
            default=["yo", "ig", "ha"],
            help="Target languages for translation (default: yo ig ha)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Limit number of lessons to translate",
        )

    def handle(self, *args, **options):
        api_key = os.getenv("SPITCH_API_KEY")
        if not api_key:
            self.stderr.write(self.style.ERROR("SPITCH_API_KEY not found in environment"))
            return

        client = Spitch()
        target_languages = options["languages"]
        limit = options["limit"]

        lessons = Lesson.objects.all().order_by("difficulty_level")
        if limit:
            lessons = lessons[:limit]

        if not lessons.exists():
            self.stdout.write(self.style.WARNING("⚠️ No lessons found to translate."))
            return

        for lesson in lessons:
            for lang in target_languages:
                if LessonTranslation.objects.filter(lesson=lesson, language=lang).exists():
                    self.stdout.write(f"✅ Skipping {lesson} ({lang}) - translation already exists.")
                    continue

                try:
                    # Translate explanation
                    translation = client.text.translate(
                        text=lesson.code_explanation,
                        source="en",
                        target=lang,
                    )

                    # Save translation
                    lt = LessonTranslation.objects.create(
                        lesson=lesson,
                        language=lang,
                        concept_text=translation.text,
                    )
                    lt.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"🎉 Translation saved for {lesson} → {lang}"
                        )
                    )

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"❌ Failed for {lesson} ({lang}): {e}")
                    )
