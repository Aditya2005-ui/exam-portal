from django.shortcuts import render, redirect, get_object_or_404
from .models import student_info, teacher_info, paper, Result, Test


# ---------------- MAIN + AUTH ----------------

def giveMeLogin(request):
    return render(request, "login.html")


def logout_user(request):
    request.session.flush()
    return redirect("giveMeLogin")


def registration(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mob = request.POST.get("mob")
        password = request.POST.get("password")

        if student_info.objects.filter(mob=mob).exists():
            return render(request, "registration.html", {"error": "Mobile already registered!"})

        student_info.objects.create(name=name, mob=mob, password=password)
        return redirect("stu_login")

    return render(request, "registration.html")


def stu_login(request):
    if request.method == "POST":
        mob = request.POST.get("mob")
        password = request.POST.get("password")

        s = student_info.objects.filter(mob=mob, password=password).first()
        if s:
            request.session["student_id"] = s.id
            request.session["student_name"] = s.name
            return redirect("student_dashboard")

        return render(request, "stu_login.html", {"error": "Invalid Mobile or Password"})

    return render(request, "stu_login.html")


def teach_login(request):
    if request.method == "POST":
        mob = request.POST.get("mob")
        password = request.POST.get("password")

        t = teacher_info.objects.filter(mob=mob, password=password).first()
        if t:
            request.session["teacher_id"] = t.id
            request.session["teacher_name"] = t.name
            return redirect("teacher_dashboard")

        return render(request, "teach_login.html", {"error": "Invalid Mobile or Password"})

    return render(request, "teach_login.html")


# ---------------- DASHBOARDS ----------------

def student_dashboard(request):
    if "student_id" not in request.session:
        return redirect("stu_login")
    return render(request, "student_dashboard.html")


def teacher_dashboard(request):
    if "teacher_id" not in request.session:
        return redirect("teach_login")
    return render(request, "teacher_dashboard.html")


# ---------------- TEACHER: TEST + QUESTIONS ----------------

def create_test(request):
    if "teacher_id" not in request.session:
        return redirect("teach_login")

    if request.method == "POST":
        test_name = request.POST.get("test_name")
        duration = request.POST.get("duration_minutes")

        Test.objects.create(test_name=test_name, duration_minutes=duration)
        return redirect("teacher_dashboard")

    return render(request, "create_test.html")


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
        return render(request, "add_question.html", {"tests": tests, "success": "Question Added ✅"})

    return render(request, "add_question.html", {"tests": tests})


def view_questions(request, test_id):
    if "teacher_id" not in request.session:
        return redirect("teach_login")

    test = get_object_or_404(Test, id=test_id)
    questions = paper.objects.filter(test_id=test_id).order_by("qno")

    return render(request, "view_questions.html", {
        "questions": questions,
        "test": test
    })
    
def teacher_tests(request):
    if "teacher_id" not in request.session:
        return redirect("teach_login")

    tests = Test.objects.all().order_by("-created_at")
    return render(request, "teacher_tests.html", {"tests": tests})



def delete_question(request, id):
    if "teacher_id" not in request.session:
        return redirect("teach_login")

    q = get_object_or_404(paper, id=id)
    test_id = q.test_id
    q.delete()
    return redirect("view_questions", test_id=test_id)


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

    # ✅ FIX: test_id send to template
    return render(request, "edit_question.html", {"q": q, "test_id": q.test_id})



# ---------------- STUDENT: SELECT TEST + EXAM ----------------

def select_test(request):
    if "student_id" not in request.session:
        return redirect("stu_login")

    tests = Test.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "select_test.html", {"tests": tests})


def start_exam(request, test_id):
    if "student_id" not in request.session:
        return redirect("stu_login")

    student_id = request.session["student_id"]

    # ✅ One attempt only PER TEST
    if Result.objects.filter(student_id=student_id, test_id=test_id).exists():
        return render(request, "already_attempted.html")

    test = get_object_or_404(Test, id=test_id)

    # ✅ Random questions
    questions = paper.objects.filter(test_id=test_id).order_by("?")

    return render(request, "start_exam.html", {
        "questions": questions,
        "exam_minutes": test.duration_minutes,
        "test_id": test_id,
        "test_name": test.test_name
    })


def submit_exam(request, test_id):
    if "student_id" not in request.session:
        return redirect("stu_login")

    student_id = request.session["student_id"]

    # ✅ security: one attempt per test
    if Result.objects.filter(student_id=student_id, test_id=test_id).exists():
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
            else:
                if int(selected) == q.correct_option:
                    correct_answers += 1
                else:
                    wrong_answers += 1

        # ✅ NEET/JEE scoring
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


def my_result(request):
    if "student_id" not in request.session:
        return redirect("stu_login")

    results = Result.objects.filter(student_id=request.session["student_id"]).select_related("test").order_by("-date_time")
    return render(request, "my_result.html", {"results": results})


# ---------------- TEACHER RESULTS ----------------

def teacher_results(request):
    if "teacher_id" not in request.session:
        return redirect("teach_login")

    results = Result.objects.select_related("student", "test").order_by("-date_time")
    return render(request, "teacher_results.html", {"results": results})
