import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from lesson.models import Lesson, LessonTranslation
from spitch import Spitch


class Command(BaseCommand):
    help = "Translate Lesson explanations into Yoruba, Igbo, Hausa using Spitch API and generate audio files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--languages",
            nargs="+",
            default=["yo", "ig", "ha"],
            help="Target languages for translation (default: yo ig ha)",
        )

    def handle(self, *args, **options):
        api_key = os.getenv("SPITCH_API_KEY", None)
        if not api_key:
            self.stderr.write(self.style.ERROR("SPITCH_API_KEY not found in environment"))
            return

        client = Spitch()
        target_languages = options["languages"]

        lessons = Lesson.objects.all()[:2]
        if not lessons.exists():
            self.stdout.write(self.style.WARNING("No lessons found to translate."))
            return

        # Map languages to default voices (you can customize this)
        default_voices = {
            "yo": "sade",   # Yoruba
            "ig": "amara", # Igbo
            "ha": "hasan",  # Hausa
        }

        for lesson in lessons:
            for lang in target_languages:
                if LessonTranslation.objects.filter(lesson=lesson, language=lang).exists():
                    self.stdout.write(f"✅ Skipping {lesson} ({lang}) - already exists.")
                    continue

                try:
                    # 1. Translate text
                    translation = client.text.translate(
                        text=lesson.code_explanation,
                        source="en",
                        target=lang,
                    )

                    # 2. Generate audio
                    voice = default_voices.get(lang, "default")
                    audio_response = client.speech.generate(
                        text=translation.text,
                        language=lang,
                        voice=voice,
                    )

                    # Save translation + audio file
                    lt = LessonTranslation(
                        lesson=lesson,
                        language=lang,
                        concept_text=translation.text,
                    )
                    # Wrap response into a Django file
                    lt.audio_file.save(
                        f"{lesson.id}_{lang}.mp3",
                        ContentFile(audio_response.read()),
                        save=True,
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"🎉 Translated + Audio saved for {lesson} → {lang}"
                        )
                    )

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"❌ Failed for {lesson} ({lang}): {e}")
                    )


        