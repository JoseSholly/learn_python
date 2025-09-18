from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from allauth.account.forms import LoginForm
from django.utils import timezone
from .models import UserProgress
from lesson.models import Lesson
from django.contrib import messages
from allauth.account.models import EmailAddress
from .forms import ResendVerificationForm
from django.contrib.auth import get_user_model
from allauth.account.models import EmailConfirmation

User = get_user_model()


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

def account_not_verified(request):
    return render(request, "account/not_verified.html")


def resend_verification_request(request):
    if request.method == "POST":
        form = ResendVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()

            if not user:
                messages.error(request, "This email is not registered.")
                return redirect("user:resend_verification_request")

            if user.is_verified:
                messages.info(request, "This email is already verified.")
                return redirect("user:resend_verification_request")

            try:
                # Get the EmailAddress object for this email
                email_address = EmailAddress.objects.filter(email=email, user=user).first()
                
                if email_address:
                    # Create and send email confirmation using the current API
                    confirmation = EmailConfirmation.create(email_address)
                    confirmation.send(request)
                    
                    messages.success(request, f"A verification link has been sent to {email}.")
                    return redirect("user:resend_verification_done")
                    
            except Exception:
                messages.error(request, "Failed to send verification email. Please try again.")
                return redirect("user:resend_verification_request")
                
    else:
        form = ResendVerificationForm()
    
    return render(request, 'account/resend_verification_request.html', {'form': form})



def resend_verification_done(request):
    return render(request, "account/resend_verification_done.html")