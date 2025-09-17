from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from allauth.account.forms import LoginForm
from django.utils import timezone
from .models import UserProgress
from lesson.models import Lesson

def landing_page(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):

    """
    Fetches all lesson objects and attaches is_completed flag for the current user.
    """
    lessons = Lesson.objects.all().order_by("difficulty_level")

    for lesson in lessons:
        progress = lesson.progress.filter(user=request.user, completed=True).exists()
        lesson.is_completed = progress

    context = {
        "lessons": lessons,
    }
    return render(request, "dashboard.html", context)



def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            try:
                # The authenticate method of the Allauth form will call your adapter
                user = form.authenticate(request)
                if user:
                    login(request, user)
                    return redirect('dashboard')  # Redirect to dashboard on successful login
            except PermissionDenied as e:
                # Catch the specific error and add it to the form for display
                form.add_error(None, str(e))
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})




@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Get or create progress for this user and lesson
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )

    # Update completion status
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    # Redirect back to lesson detail (or anywhere you want)
    return redirect("lesson:lesson_detail", lesson_id=lesson.id)
