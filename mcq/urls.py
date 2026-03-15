from django.urls import path
from . import views


urlpatterns = [

    # ======================
    # HOME + AUTH
    # ======================

    path("", views.giveMeLogin, name="home"),

    path("login/", views.giveMeLogin, name="giveMeLogin"),
    path("student/login/", views.stu_login, name="stu_login"),
    path("teacher/login/", views.teach_login, name="teach_login"),

    path("registration/", views.registration, name="registration"),
    path("logout/", views.logout_user, name="logout"),


    # ======================
    # STUDENT SECTION
    # ======================

    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),

    path("student/tests/", views.select_test, name="select_test"),

    path("student/start-exam/<int:test_id>/",
         views.start_exam,
         name="start_exam"),

    path("student/submit-exam/<int:test_id>/",
         views.submit_exam,
         name="submit_exam"),

    path("student/results/", views.my_result, name="my_result"),


    # ======================
    # TEACHER SECTION
    # ======================

    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),

    path("teacher/create-test/", views.create_test, name="create_test"),

    path("teacher/add-question/", views.add_question, name="add_question"),

    path("teacher/tests/", views.teacher_tests, name="teacher_tests"),

    path("teacher/view-questions/<int:test_id>/",
         views.view_questions,
         name="view_questions"),

    path("teacher/edit-question/<int:id>/",
         views.edit_question,
         name="edit_question"),

    path("teacher/delete-question/<int:id>/",
         views.delete_question,
         name="delete_question"),

    path("teacher/results/", views.teacher_results, name="teacher_results"),
]