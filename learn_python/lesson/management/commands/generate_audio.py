import os
import logging
from django.core.management.base import BaseCommand
from lesson.models import LessonTranslation
from spitch import Spitch
import cloudinary.uploader



logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate audio for all Lesson translations without audio."

    def handle(self, *args, **options):
        api_key = os.getenv("SPITCH_API_KEY", None)
        if not api_key:
            msg = "SPITCH_API_KEY not found in environment"
            self.stderr.write(self.style.ERROR(msg))
            logger.error(msg)
            return

        client = Spitch()

        # Map languages to default voices
        default_voices = {
            "yo": "sade",   # Yoruba
            "ig": "amara",  # Igbo
            "ha": "hasan",  # Hausa
            "en": "default",  # English fallback
        }

        translations = LessonTranslation.objects.all()
        for lt in translations:
            if lt.audio:
                msg = f"Skipping {lt} — audio already exists ({lt.audio.url})"
                self.stdout.write(self.style.NOTICE(msg))
                logger.info(msg)
                continue

            lang = lt.language
            voice = default_voices.get(lang, "default")

            try:
                self.stdout.write(f"Generating audio for {lt} ...")
                logger.info(f"Generating audio for {lt} (lang={lang}, voice={voice})")

                audio_response = client.speech.generate(
                    text=lt.concept_text,
                    language=lang,
                    voice=voice,
                )

                # Direct upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    audio_response,
                    resource_type="video",  # Audio uses video resource type
                    folder='audio',
                    public_id=f"{lt.lesson.id}_{lang}",
                    format="mp3"
                )

                # Save the Cloudinary URL to your model
                lt.audio = upload_result['secure_url']
                lt.save()

                msg = f"Audio generated for {lt} → {lt.audio}"
                self.stdout.write(self.style.SUCCESS(msg))
                logger.info(msg)

            except Exception as e:
                error_msg = f"Failed for {lt}: {e}"
                self.stderr.write(self.style.ERROR(error_msg))
                logger.error(error_msg, exc_info=True)
