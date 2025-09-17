from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "lesson/<int:lesson_id>/complete/",
        views.complete_lesson,
        name="complete_lesson",
    ),
]
