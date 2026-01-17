from django.db import models

class student_info(models.Model):
    name = models.CharField(max_length=100)
    mob = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class teacher_info(models.Model):
    name = models.CharField(max_length=100)
    mob = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name


# ✅ NEW MODEL (Test/Paper)
class Test(models.Model):
    test_name = models.CharField(max_length=120)
    duration_minutes = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.test_name


class paper(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)   # ✅ ADD THIS

    CHOICES = (
        (1, "Option 1"),
        (2, "Option 2"),
        (3, "Option 3"),
        (4, "Option 4"),
    )

    qno = models.IntegerField()
    question = models.CharField(max_length=300)

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct_option = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return self.question


class Result(models.Model):
    student = models.ForeignKey(student_info, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)   # ✅ NEW (per test attempt)

    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    score = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name
