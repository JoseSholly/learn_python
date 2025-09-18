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
    path("account/not-verified/", views.account_not_verified, name="account_not_verified"),
    path("account/resend-verification/", views.resend_verification_request, name="resend_verification_request"),
    path("account/resend-verification/done/", views.resend_verification_done, name="resend_verification_done"),
]
