import pytest
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.urls import reverse
from lesson.models import Lesson, LessonTranslation


@pytest.mark.django_db
@patch("lesson.management.commands.generate_audio.cloudinary.uploader.upload")
@patch("lesson.management.commands.generate_audio.Spitch")
@patch("lesson.management.commands.generate_translation.Spitch")
def test_integration_flow(mock_spitch_translate, mock_spitch_audio, mock_upload, client, django_user_model):
    # --- Setup ---
    # Mock translation
    mock_translate_client = MagicMock()
    mock_translate_client.text.translate.return_value.text = "Translated explanation"
    mock_spitch_translate.return_value = mock_translate_client

    # Mock audio
    mock_audio_client = MagicMock()
    mock_audio_client.speech.generate.return_value = b"fake audio bytes"
    mock_spitch_audio.return_value = mock_audio_client

    # Mock Cloudinary upload
    mock_upload.return_value = {"secure_url": "http://cloudinary.com/fake_audio.mp3"}

    # Create lesson
    lesson = Lesson.objects.create(
        topic="Intro to Python",
        code_explanation="This is a test explanation",
        code_example="test=1",
        difficulty_level='1',
    )

    # Create and login user
    user = django_user_model.objects.create_user(email="sampleuser@example.com", password="testpass")
    client.login(email="sampleuser@example.com", password="testpass")

    # --- Run commands ---
    call_command("generate_translation", "--languages", "yo")
    call_command("generate_audio")

    # --- Request lesson detail page ---
    url = reverse("lesson:lesson_detail", args=[lesson.id])
    response = client.get(url)

    # --- Assertions ---
    assert response.status_code == 200
    content = response.content.decode()

    # Lesson info
    assert "Intro to Python" in content
    
    # Translated text
    assert "Translated explanation" in content

    # Audio URL embedded
    assert "http://cloudinary.com/fake_audio" in content
    assert "<audio" in content
