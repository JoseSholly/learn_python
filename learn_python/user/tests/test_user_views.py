# tests/test_views.py
import pytest
from django.urls import reverse
from django.utils import timezone
from user.models import UserProgress
from lesson.models import Lesson


@pytest.mark.django_db
def test_landing_page(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert "home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_dashboard_requires_login(client):
    url = reverse("user:dashboard")
    response = client.get(url)
    # should redirect to login
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_with_lessons(client, django_user_model):
    user = django_user_model.objects.create_user(email="test@example.com", password="pass123")
    lesson = Lesson.objects.create(
        topic="Sample Lesson",
        subtopic="Basics",
        code_example="Explanation",
        code_explanation="print('hi')",
        difficulty_level='1',
    )

    client.login(email="test@example.com", password="pass123")
    url = reverse("user:dashboard")
    response = client.get(url)

    assert response.status_code == 200
    assert "dashboard.html" in [t.name for t in response.templates]
    assert "Sample Lesson" in response.content.decode()


@pytest.mark.django_db
def test_complete_lesson_marks_progress(client, django_user_model):
    user = django_user_model.objects.create_user(email="student@example.com", password="pass123")
    lesson = Lesson.objects.create(
        topic="Lesson 1",
        subtopic="Intro",
        code_example="Learn basics",
        code_explanation="print('hello')",
        difficulty_level=1,
    )

    client.login(email="student@example.com", password="pass123")
    url = reverse("user:complete_lesson", args=[lesson.id])
    response = client.post(url)

    # check redirect back to lesson detail
    assert response.status_code == 302
    assert reverse("lesson:lesson_detail", args=[lesson.id]) in response.url

    # check progress updated
    progress = UserProgress.objects.get(user=user, lesson=lesson)
    assert progress.completed is True
    assert progress.completed_at is not None
    assert progress.completed_at <= timezone.now()
