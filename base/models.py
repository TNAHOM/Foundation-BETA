import random

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
	phone_number = models.IntegerField(null=True, blank=True)
	description = models.TextField()
	registered = models.DateField(auto_now_add=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	sub_city = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.name
	class Meta:
		pass

class ClassGrade(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	class_grade = models.IntegerField()
	section = models.CharField(max_length=255)
	
	def __str__(self):
		return f'{self.class_grade} -- {self.section} -- {self.school}'
	
	class Meta:
		# cant have same school, class grade, section
		unique_together = [['school', 'class_grade', 'section']]
	
class Student(User):
	school_name = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
	class_grade = models.ForeignKey(ClassGrade, on_delete=models.SET_NULL, null=True,blank=True)
	sex = models.CharField(choices=SEX, max_length=6, default='M')
	student_id = models.IntegerField(null=True, blank=False, unique=True)
	
	class Meta:
		pass
	
	def save(self, *args, **kwargs):
		if not self.student_id:
			self.generate_unique_student_id()
		super().save(*args, **kwargs)
	
	def generate_unique_student_id(self):
		unique_id = random.randint(1000, 99999)
		while Student.objects.filter(student_id=unique_id).exists():
			unique_id = random.randint(1000, 99999)
		self.student_id = unique_id
		self.save()


class Teacher(User):
	phone_number = models.BigIntegerField(null=True, blank=True)
	school_name = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
	subject = models.CharField(max_length=100, choices=SUBJECT, default='ENG')
	sex = models.CharField(choices=SEX, max_length=6, default='M')
	class_grade = models.ManyToManyField(ClassGrade, blank=True)
	
	class Meta:
		pass


class Exam(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	school_name = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='teacher')
	unique_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
	exam_code_f = models.IntegerField(null=True, blank=False, unique=True)
	exam_code_b = models.IntegerField(null=True, blank=False, unique=True)
	choose_answer = models.CharField(max_length=3000, null=True, blank=True)
	truefalse_answer = models.CharField(max_length=1028, null=True, blank=True)
	fillblank_answer = models.CharField(max_length=1028, null=True, blank=True)
	matching_answer = models.CharField(max_length=1028, null=True, blank=True)
	no_of_questions = models.IntegerField()
	created = models.DateField(auto_now_add=True)
	start_time = models.DateField()
	
	class Meta:
		# add '-' this to make it ascending ;otherwise it's descending
		ordering = ['-start_time']
	
	def __str__(self):
		return f'{self.teacher.subject}, {self.unique_name}'
	
class Score(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	student_score = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_score')
	subject = models.ForeignKey(Exam, on_delete=models.CASCADE)
	score_exam_code_f = models.IntegerField(null=True, blank=True)
	score_exam_code_b = models.IntegerField(null=True, blank=True)
	score = models.IntegerField()
	display = models.BooleanField(default=False)
	finished = models.DateField(auto_now_add=True)
	incorrect_ans = models.CharField(max_length=1000, null=True, blank=True)
	incorrect_ans_num = models.CharField(max_length=1000, null=True, blank=True)
	disqualified_ans = models.CharField(max_length=1000, null=True, blank=True)
	disqualified_ans_num = models.CharField(max_length=1000, null=True, blank=True)
	
	class Meta:
		ordering = ['finished']
	
	def __str__(self):
		return f'{self.student_score} ---  {self.subject.teacher.subject} --- {self.score} --- {self.finished}'
	
	
class Reports(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)
	
	class Meta:
		ordering = ['time']
	
	def __str__(self):
		return f'{self.user.role} - {self.user.email} - {self.user.name} - {self.time}'
