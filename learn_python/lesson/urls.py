from django.urls import path
from . import views
app_name = "lesson"
urlpatterns = [
    path('lesson/<int:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
]