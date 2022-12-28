from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
import uuid

# Create your models here.
ROLES = [
	('Student', 'Student'),
	('Teacher', 'Teacher'),
	('Parents', 'Parents'),
	('School Administrator', 'School Administrator'),
	('Super User', 'Super User')
]
SUBJECT = [
	('English', 'ENG'),
	('Mathematics', 'MAT'),
	('Physics', 'PHY'),
	('Chemistry', 'CHE'),
	('Biology', 'BIO'),
	('SAT', 'SAT'),
	('Civics', 'CIV')
]
CLASS_GRADE = [
	(9, 9),
	(10, 10),
	(11, 11),
	(12, 12)
]
SECTION = [
	('A', 'A'),
	('B', 'B'),
	('C', 'C'),
	('D', 'D'),
	('E', 'E'),
	('F', 'F'),
	('G', 'G')
]

SEX = [
	('M', 'Male'),
	('F', 'Female')
]

class User(AbstractUser):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	role = models.CharField(max_length=30, choices=ROLES, default='Student')
	
	website = models.URLField(max_length=300, null=True, blank=True)
	facebook = models.URLField(max_length=300, null=True, blank=True)
	twitter = models.URLField(max_length=300, null=True, blank=True)
	linkedin = models.URLField(max_length=300, null=True, blank=True)
	Instagram = models.URLField(max_length=300, null=True, blank=True)

	
	# replaces the username field with email
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'role']

class School(User):
	class_grade = MultiSelectField(choices=CLASS_GRADE, max_length=10, max_choices=4)
	phone_num = models.IntegerField()
	description = models.TextField()
	registered = models.DateTimeField(auto_now_add=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	sub_city = models.CharField(max_length=255, null=True, blank=True)

	# Bio-->Image

	class Meta:
		pass
	
class Grade(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	grade = models.IntegerField()
	
	def __str__(self):
		return str(self.grade)
	
	class Meta:
		pass

class Section(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
	section = models.CharField(max_length=1)
	
	def __str__(self):
		return f'{str(self.grade)}- {self.section}'
	
	class Meta:
		pass

class Student(User):
	school_name = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	class_grade = models.IntegerField()
	section = models.CharField(max_length=1)
	sex = models.CharField(choices=SEX, max_length=6, default='M')
	
	class Meta:
		pass

	
class Teacher(User):
	phone_num = models.IntegerField()
	school_name = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	subject = models.CharField(max_length=100, choices=SUBJECT, default='ENG')
	class_grade = models.IntegerField()
	section = models.CharField(max_length=1)
	sex = models.CharField(choices=SEX, max_length=6, default='M')

	
	class Meta:
		pass

class Exam(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	school_name = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True, blank=True, related_name='teacher')
	unique_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
	subject = models.CharField(max_length=20, choices=SUBJECT, default='ENG')
	choose_answer = models.CharField(max_length=300, null=False, blank=False)
	truefalse_answer = models.CharField(max_length=50, null=False, blank=False)
	fillblank_answer = models.CharField(max_length=512, null=False, blank=False)
	no_of_questions = models.IntegerField(null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(null=False, blank=False)
	end_time = models.DateTimeField(null=False, blank=False)
	
	class Meta:
		# add '-' this to make it ascending ;otherwise it's descending
		ordering = ['-start_time']
	
	def __str__(self):
		return f'{self.subject}, {self.unique_name}'
	
class Score(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	student_score = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_score')
	subject = models.ForeignKey(Exam, on_delete=models.CASCADE)
	score = models.IntegerField()
	checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='checkedby')
	display = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{self.student_score} ---  {self.subject} --- {self.score}'
	