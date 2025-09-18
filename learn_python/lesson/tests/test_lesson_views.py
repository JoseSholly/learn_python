import pytest
from django.urls import reverse
from lesson.models import Lesson
from user.models import User, UserProgress


@pytest.mark.django_db
def test_lesson_detail_view_renders(client, django_user_model):
    user = django_user_model.objects.create_user(email="student@example.com", password="pass123")

    lesson = Lesson.objects.create(
        topic="Python",
        subtopic="Variables",
        code_example="x = 5",
        code_explanation="This assigns 5 to x.",
        difficulty_level="1",
    )

    client.login(email="student@example.com", password="pass123")

    url = reverse("lesson:lesson_detail", args=[lesson.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "lessons/lesson_detail.html" in [t.name for t in response.templates]
    assert "Variables" in response.content.decode()


@pytest.mark.django_db
def test_lesson_detail_view_marks_completion(client, django_user_model):
    user = django_user_model.objects.create_user(email="student@example.com", password="pass123")
    lesson = Lesson.objects.create(
        topic="Python",
        subtopic="Loops",
        code_example="for i in range(5): print(i)",
        code_explanation="This prints 0 to 4.",
        difficulty_level="2",
    )

    # Mark lesson completed
    UserProgress.objects.create(user=user, lesson=lesson, completed=True)

    client.login(email="student@example.com", password="pass123")
    url = reverse("lesson:lesson_detail", args=[lesson.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "lessons/lesson_detail.html" in [t.name for t in response.templates]

    # The context must include is_completed = True
    assert response.context["is_completed"] is True


@pytest.mark.django_db
def test_lesson_detail_view_404_if_not_exist(client, django_user_model):
    user = django_user_model.objects.create_user(email="student@example.com", password="pass123")
    client.login(email="student@example.com", password="pass123")

    url = reverse("lesson:lesson_detail", args=[999])  # non-existent ID
    response = client.get(url)
    assert response.status_code == 404
