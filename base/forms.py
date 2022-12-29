from django import forms
from .models import Student, Teacher, Exam, School
from django.contrib.auth.forms import UserCreationForm


class RegisterStudent(UserCreationForm):
	class Meta:
		model = Student
		fields = ['name', 'username', 'email', 'sex', 'password1', 'password2', 'section', 'class_grade']
		
class RegisterTeacher(UserCreationForm):
	class Meta:
		model = Teacher
		fields = ['name', 'username', 'email', 'sex','password1', 'password2', 'subject', 'class_grade']

class RegisterParent(forms.ModelForm):
	class Meta:
		model = Teacher
		exclude = ['announcement']

class CreateExam(forms.ModelForm):
	class Meta:
		model = Exam
		fields = ['unique_name', 'no_of_questions', 'start_time', 'end_time']

class RegisterSchool(UserCreationForm):
	class Meta:
		model = School
		fields = ['name', 'username', 'email' ,'phone_number', 'password1', 'password2', 'description', 'city', 'sub_city']

		
class EditAccountSchool(forms.ModelForm):
	class Meta:
		model = School
		fields = ['username', 'email', 'class_grade', 'phone_number', 'description', 'website', 'facebook', 'twitter', 'Instagram', 'linkedin']