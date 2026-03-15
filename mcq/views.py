from django.shortcuts import render, redirect, get_object_or_404
from .models import student_info, teacher_info, paper, Result, Test


# =========================
# LOGIN PAGE
# =========================

def giveMeLogin(request):
    return render(request, "login.html")


def logout_user(request):
    request.session.flush()
    return redirect("home")


# =========================
# STUDENT REGISTRATION
# =========================

def registration(request):

    if request.method == "POST":

        name = request.POST.get("name")
        mob = request.POST.get("mob")
        password = request.POST.get("password")

        if student_info.objects.filter(mob=mob).exists():
            return render(request, "registration.html",
                          {"error": "Mobile already registered!"})

        student_info.objects.create(
            name=name,
            mob=mob,
            password=password
        )

        return redirect("stu_login")

    return render(request, "registration.html")


# =========================
# STUDENT LOGIN
# =========================

def stu_login(request):

    if request.method == "POST":

        mob = request.POST.get("mob")
        password = request.POST.get("password")

        s = student_info.objects.filter(
            mob=mob,
            password=password
        ).first()

        if s:
            request.session["student_id"] = s.id
            request.session["student_name"] = s.name
            return redirect("student_dashboard")

        return render(request, "stu_login.html",
                      {"error": "Invalid Mobile or Password"})

    return render(request, "stu_login.html")


# =========================
# TEACHER LOGIN
# =========================

def teach_login(request):

    if request.method == "POST":

        mob = request.POST.get("mob")
        password = request.POST.get("password")

        t = teacher_info.objects.filter(
            mob=mob,
            password=password
        ).first()

        if t:
            request.session["teacher_id"] = t.id
            request.session["teacher_name"] = t.name
            return redirect("teacher_dashboard")

        return render(request, "teach_login.html",
                      {"error": "Invalid Mobile or Password"})

    return render(request, "teach_login.html")


# =========================
# STUDENT DASHBOARD
# =========================

def student_dashboard(request):

    if "student_id" not in request.session:
        return redirect("stu_login")

    return render(request, "student_dashboard.html")


# =========================
# TEACHER DASHBOARD
# =========================

def teacher_dashboard(request):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    return render(request, "teacher_dashboard.html")


# =========================
# CREATE TEST
# =========================

def create_test(request):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    if request.method == "POST":

        test_name = request.POST.get("test_name")
        duration = request.POST.get("duration_minutes")

        Test.objects.create(
            test_name=test_name,
            duration_minutes=duration
        )

        return redirect("teacher_dashboard")

    return render(request, "create_test.html")


# =========================
# ADD QUESTION
# =========================

def add_question(request):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    tests = Test.objects.filter(is_active=True).order_by("-created_at")

    if request.method == "POST":

        test_id = request.POST.get("test_id")

        paper.objects.create(
            test_id=test_id,
            qno=request.POST.get("qno"),
            question=request.POST.get("question"),
            option1=request.POST.get("option1"),
            option2=request.POST.get("option2"),
            option3=request.POST.get("option3"),
            option4=request.POST.get("option4"),
            correct_option=request.POST.get("correct_option"),
        )

        return render(
            request,
            "add_question.html",
            {"tests": tests, "success": "Question Added Successfully"}
        )

    return render(request, "add_question.html", {"tests": tests})


# =========================
# VIEW QUESTIONS
# =========================

def view_questions(request, test_id):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    test = get_object_or_404(Test, id=test_id)

    questions = paper.objects.filter(
        test_id=test_id
    ).order_by("qno")

    return render(
        request,
        "view_questions.html",
        {"questions": questions, "test": test}
    )


# =========================
# TEACHER TEST LIST
# =========================

def teacher_tests(request):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    tests = Test.objects.all().order_by("-created_at")

    return render(request, "teacher_tests.html", {"tests": tests})


# =========================
# DELETE QUESTION
# =========================

def delete_question(request, id):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    q = get_object_or_404(paper, id=id)

    test_id = q.test_id

    q.delete()

    return redirect("view_questions", test_id=test_id)


# =========================
# EDIT QUESTION
# =========================

def edit_question(request, id):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    q = get_object_or_404(paper, id=id)

    if request.method == "POST":

        q.qno = request.POST.get("qno")
        q.question = request.POST.get("question")
        q.option1 = request.POST.get("option1")
        q.option2 = request.POST.get("option2")
        q.option3 = request.POST.get("option3")
        q.option4 = request.POST.get("option4")
        q.correct_option = request.POST.get("correct_option")

        q.save()

        return redirect("view_questions", test_id=q.test_id)

    return render(request, "edit_question.html", {
        "q": q,
        "test_id": q.test_id
    })


# =========================
# SELECT TEST
# =========================

def select_test(request):

    if "student_id" not in request.session:
        return redirect("stu_login")

    tests = Test.objects.filter(is_active=True).order_by("-created_at")

    return render(request, "select_test.html", {"tests": tests})


# =========================
# START EXAM
# =========================

def start_exam(request, test_id):

    if "student_id" not in request.session:
        return redirect("stu_login")

    student_id = request.session["student_id"]

    if Result.objects.filter(student_id=student_id,
                             test_id=test_id).exists():
        return render(request, "already_attempted.html")

    test = get_object_or_404(Test, id=test_id)

    questions = paper.objects.filter(test_id=test_id).order_by("?")

    return render(
        request,
        "start_exam.html",
        {
            "questions": questions,
            "exam_minutes": test.duration_minutes,
            "test_id": test_id,
            "test_name": test.test_name
        }
    )


# =========================
# SUBMIT EXAM
# =========================

def submit_exam(request, test_id):

    if "student_id" not in request.session:
        return redirect("stu_login")

    student_id = request.session["student_id"]

    if Result.objects.filter(student_id=student_id,
                             test_id=test_id).exists():
        return render(request, "already_attempted.html")

    if request.method == "POST":

        questions = paper.objects.filter(test_id=test_id)

        total_questions = questions.count()
        correct_answers = 0
        wrong_answers = 0
        not_attempted = 0

        for q in questions:

            selected = request.POST.get(f"q{q.id}")

            if selected is None:
                not_attempted += 1

            elif int(selected) == q.correct_option:
                correct_answers += 1

            else:
                wrong_answers += 1

        score = (correct_answers * 4) - (wrong_answers * 1)

        Result.objects.create(
            student_id=student_id,
            test_id=test_id,
            total_questions=total_questions,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
            score=score
        )

        return render(request, "result.html", {
            "total": total_questions,
            "correct": correct_answers,
            "wrong": wrong_answers,
            "not_attempted": not_attempted,
            "score": score
        })

    return redirect("start_exam", test_id=test_id)


# =========================
# STUDENT RESULT PAGE
# =========================

def my_result(request):

    if "student_id" not in request.session:
        return redirect("stu_login")

    results = Result.objects.filter(
        student_id=request.session["student_id"]
    ).select_related("test").order_by("-date_time")

    return render(request, "my_result.html", {"results": results})


# =========================
# TEACHER RESULT PAGE
# =========================

def teacher_results(request):

    if "teacher_id" not in request.session:
        return redirect("teach_login")

    results = Result.objects.select_related(
        "student",
        "test"
    ).order_by("-date_time")

    return render(request, "teacher_results.html", {"results": results})