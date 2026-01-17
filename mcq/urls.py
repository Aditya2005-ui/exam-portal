from django.urls import path
from . import views

urlpatterns = [
    path("givemelogin/", views.giveMeLogin, name="giveMeLogin"),
    path("stu_login/", views.stu_login, name="stu_login"),
    path("teach_login/", views.teach_login, name="teach_login"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.logout_user, name="logout"),

    # student
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("select_test/", views.select_test, name="select_test"),
    path("start_exam/<int:test_id>/", views.start_exam, name="start_exam"),
    path("submit_exam/<int:test_id>/", views.submit_exam, name="submit_exam"),
    path("my_result/", views.my_result, name="my_result"),

    # teacher
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("create_test/", views.create_test, name="create_test"),
    path("add_question/", views.add_question, name="add_question"),
    path("view_questions/<int:test_id>/", views.view_questions, name="view_questions"),
    path("delete_question/<int:id>/", views.delete_question, name="delete_question"),
    path("edit_question/<int:id>/", views.edit_question, name="edit_question"),
    path("teacher_tests/", views.teacher_tests, name="teacher_tests"),
    path("teacher_results/", views.teacher_results, name="teacher_results"),
]
