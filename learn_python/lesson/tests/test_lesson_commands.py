import pytest
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from lesson.models import Lesson, LessonTranslation





@pytest.mark.django_db
@patch("lesson.management.commands.generate_translation.Spitch")
def test_generate_translation_command(mock_spitch, capsys):
    # Setup mock translation
    mock_client = MagicMock()
    mock_client.text.translate.return_value.text = "Translated text"
    mock_spitch.return_value = mock_client

    # Create lesson
    lesson = Lesson.objects.create(
        topic="Intro to Python",
        code_explanation="This is a test explanation",
        code_example="print('hello')",
        difficulty_level='1',
    )

    # Run command
    call_command("generate_translation", "--languages", "yo")

    # Capture output
    captured = capsys.readouterr()
    assert "🎉 Translation saved" in captured.out

    # Verify translation created
    translation = LessonTranslation.objects.get(lesson=lesson, language="yo")
    assert translation.concept_text == "Translated text"


@pytest.mark.django_db
@patch("lesson.management.commands.generate_audio.cloudinary.uploader.upload")
@patch("lesson.management.commands.generate_audio.Spitch")
def test_generate_audio_command(mock_spitch, mock_upload, capsys):
    # Setup mock speech generation
    mock_client = MagicMock()
    mock_client.speech.generate.return_value = b"fake audio bytes"
    mock_spitch.return_value = mock_client

    # Setup mock cloudinary upload
    mock_upload.return_value = {"secure_url": "http://cloudinary.com/fake_audio.mp3"}

    # Create translation without audio
    lesson = Lesson.objects.create(
        topic="Intro to Python",
        subtopic= "Python Introduction",
        code_explanation="This is a test explanation",
        code_example="print('hello')",
        difficulty_level='1',
    )
    translation = LessonTranslation.objects.create(
        lesson=lesson,
        language="yo",
        concept_text="Translated text"
    )

    # Run command
    call_command("generate_audio")

    # Capture output
    captured = capsys.readouterr()
    assert "Audio generated" in captured.out

    # Verify audio URL saved
    translation.refresh_from_db()
    assert translation.audio.url == "http://cloudinary.com/fake_audio"


    