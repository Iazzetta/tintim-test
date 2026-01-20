from django.urls import path

from . import views

urlpatterns = [
    path("join-course", views.join_course, name="join_course"),
    path("set-student-grade", views.set_student_grade, name="set_student_grade"),
]