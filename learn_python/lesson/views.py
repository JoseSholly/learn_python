# In your views.py file
from django.shortcuts import render, get_object_or_404
from .models import Lesson

def lesson_detail_view(request, lesson_id):
    """
    Displays the details of a specific lesson.
    """
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    context = {
        'lesson': lesson,
    }
    return render(request, 'lessons/lesson_detail.html', context)