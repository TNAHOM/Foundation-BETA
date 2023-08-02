from django import forms
from .models import Student, Teacher, Exam, School, ClassGrade
from django.contrib.auth.forms import UserCreationForm

class RegisterStudent(UserCreationForm):
  class Meta:
    model = Student
    fields = ['name', 'email','sex', 'password1', 'password2']
    
class RegisterTeacher(UserCreationForm):
  class Meta:
    model = Teacher
    fields = ['name', 'email', 'sex','password1', 'password2', 'class_grade']

class CreateExam(forms.ModelForm):
  class Meta:
    model = Exam
    fields = ['unique_name', 'no_of_questions', 'start_time']

class RegisterSchool(UserCreationForm):
  class Meta:
    model = School
    fields = ['name', 'email','username' ,'phone_number', 'password1', 'password2', 'description', 'city', 'sub_city']

    
class EditAccountSchool(forms.ModelForm):
  class Meta:
    model = School
    fields = ['username', 'email', 'phone_number', 'description', 'website', 'facebook', 'twitter', 'Instagram', 'linkedin']


class EditAccountTeacher(forms.ModelForm):
  class Meta:
    model = School
    fields = ['username', 'email', 'phone_number', 'website', 'facebook', 'twitter', 'Instagram', 'linkedin']


class RegisterClass(forms.ModelForm):
  class Meta:
    model = ClassGrade
    fields = ['class_grade']
