from django.contrib import admin
from .models import teacher_info, student_info, paper, Result, Test

admin.site.register(teacher_info)
admin.site.register(student_info)
admin.site.register(Test)      
admin.site.register(paper)
admin.site.register(Result)
