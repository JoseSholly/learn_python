import pytest
from django.utils import timezone
from django.db import IntegrityError
from user.models import User, UserProgress
from lesson.models import Lesson


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="testuser@example.com",
        password="securepassword123"
    )
    assert user.id is not None
    assert user.email == "testuser@example.com"
    assert user.is_verified is False
    assert str(user) == "testuser@example.com"


@pytest.mark.django_db
def test_superuser_creation():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123"
    )
    assert admin.is_superuser is True
    assert admin.is_staff is True
    assert admin.email == "admin@example.com"


@pytest.mark.django_db
def test_user_progress_creation():
    user = User.objects.create_user(
        email="learner@example.com", password="password123"
    )
    lesson = Lesson.objects.create(
        topic="Python Basics",
        subtopic="Variables",
        code_example="x = 5",
        code_explanation="Assigns 5 to x",
        difficulty_level="1"
    )
    progress = UserProgress.objects.create(
        user=user,
        lesson=lesson,
        completed=True,
        completed_at=timezone.now()
    )

    assert progress.id is not None
    assert progress.user == user
    assert progress.lesson == lesson
    assert progress.completed is True
    assert "✅ Completed" in str(progress)  # uses __str__


@pytest.mark.django_db
def test_user_progress_in_progress_str():
    user = User.objects.create_user(
        email="progress@example.com", password="testpass"
    )
    lesson = Lesson.objects.create(
        topic="Python Loops",
        subtopic="For Loop",
        code_example="for i in range(5): print(i)",
        code_explanation="Loop example",
        difficulty_level="1"
    )
    progress = UserProgress.objects.create(
        user=user,
        lesson=lesson,
        completed=False
    )
    assert "⏳ In Progress" in str(progress)


@pytest.mark.django_db
def test_user_progress_uniqueness():
    user = User.objects.create_user(
        email="unique@example.com", password="pass123"
    )
    lesson = Lesson.objects.create(
        topic="Python Functions",
        subtopic="Defining Functions",
        code_example="def greet(): print('Hello')",
        code_explanation="Defines a greet function",
        difficulty_level="2"
    )

    UserProgress.objects.create(user=user, lesson=lesson, completed=False)

    with pytest.raises(IntegrityError):
        # Duplicate progress entry for same user + lesson
        UserProgress.objects.create(user=user, lesson=lesson, completed=True)
