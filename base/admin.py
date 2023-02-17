from django.contrib import admin
from .models import User, Exam, Score, Student, Teacher, School\
	, ClassGrade, Reports

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(School)

admin.site.register(Exam)
admin.site.register(Score)

admin.site.register(ClassGrade)
admin.site.register(Reports)