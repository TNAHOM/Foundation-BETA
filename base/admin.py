from django.contrib import admin
from .models import User, Exam, Score, Student, Teacher, School\
	, Grade, Section

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(School)

admin.site.register(Exam)
admin.site.register(Score)

admin.site.register(Grade)
admin.site.register(Section)