import pytest
from django.db import IntegrityError
from lesson.models import Lesson, LessonTranslation
from django.urls import reverse


@pytest.mark.django_db
def test_create_lesson():
    lesson = Lesson.objects.create(
        topic="Python Basics",
        subtopic="Variables",
        code_example="x = 5",
        code_explanation="This assigns 5 to x",
        difficulty_level="1"
    )

    assert lesson.id is not None
    assert lesson.topic == "Python Basics"
    assert lesson.subtopic == "Variables"
    assert str(lesson) == "Python Basics - Variables"


@pytest.mark.django_db
def test_create_translation_for_lesson():
    lesson = Lesson.objects.create(
        topic="Python Loops",
        subtopic="For Loop",
        code_example="for i in range(5): print(i)",
        code_explanation="This prints numbers 0–4",
        difficulty_level="2"
    )
    translation = LessonTranslation.objects.create(
        lesson=lesson,
        language="yo",
        concept_text="Eyi ni bi a ṣe n lo 'for loop' ni Python.",
        audio=None  # optional
    )

    assert translation.id is not None
    assert translation.lesson == lesson
    assert translation.language == "yo"
    assert "for loop" in translation.concept_text
    assert str(translation) == "For Loop (Yoruba)"  # uses subtopic + get_language_display()


@pytest.mark.django_db
def test_translation_requires_language():
    lesson = Lesson.objects.create(
        topic="Python Conditions",
        subtopic="If Statement",
        code_example="if x > 0: print('Positive')",
        code_explanation="Checks if x is positive",
        difficulty_level="1"
    )

    with pytest.raises(IntegrityError):
        LessonTranslation.objects.create(
            lesson=lesson,
            language=None,  # missing required field
            concept_text="Missing language"
        )


@pytest.mark.django_db
def test_translation_uniqueness_constraint():
    lesson = Lesson.objects.create(
        topic="Python Functions",
        subtopic="Defining Functions",
        code_example="def greet(): print('Hello')",
        code_explanation="Defines a function that prints Hello",
        difficulty_level="2"
    )

    LessonTranslation.objects.create(
        lesson=lesson,
        language="ig",
        concept_text="Nke a bụ nkọwa banyere ọrụ."
    )

    with pytest.raises(IntegrityError):
        # Duplicate translation for same lesson + same language
        LessonTranslation.objects.create(
            lesson=lesson,
            language="ig",
            concept_text="Duplicate translation"
        )
@pytest.mark.django_db
def test_duplicate_translation_not_allowed():
    lesson = Lesson.objects.create(
        topic="Python Functions",
        subtopic="Defining Functions",
        code_example="def greet(): print('Hello')",
        code_explanation="Defines a function that prints Hello",
        difficulty_level="2"
    )
    LessonTranslation.objects.create(lesson=lesson, language="yo", concept_text="Translated text")
    
    with pytest.raises(Exception):
        LessonTranslation.objects.create(lesson=lesson, language="yo", concept_text="Translated another text")

@pytest.mark.django_db
def test_lesson_detail_404(client, django_user_model):
    user = django_user_model.objects.create_user(email="student@example.com", password="pass123")
    client.login(email="student@example.com", password="pass123")

    url = reverse("lesson:lesson_detail", args=[999])  # Nonexistent lesson
    response = client.get(url)
    assert response.status_code == 404