from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from allauth.account.forms import LoginForm # Assuming you are using Django-Allauth

from user.models import UserProgress
from lesson.models import Lesson

def landing_page(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):

    """
    Fetches all lesson objects and passes them to the template for display.
    """
    # Fetch all lessons from the database
    lessons = Lesson.objects.all().order_by('difficulty_level',)
    
    context = {
        'lessons': lessons,
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