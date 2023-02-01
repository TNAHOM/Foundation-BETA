from django.shortcuts import render, redirect
from .models import User, Exam, Score, Teacher, Student, School, Grade, Section
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterTeacher, RegisterStudent, \
	CreateExam, RegisterSchool, EditAccountSchool
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .utilities import squash, generate_qrcode
from django.db.models import Q

from .decorater import allowed_user
from docxtpl import DocxTemplate, InlineImage
from django.http import HttpResponse


def handler404(request, exception):
	return render(request, 'error/404.html', status=404)

def handler400(request, exception):
	return render(request, 'error/400.html', status=400)

def handler403(request, exception):
	return render(request, 'error/403.html', status=403)

def handler500(request):
	return render(request, 'error/500.html', status=500)

@login_required(login_url='login')
@allowed_user(allowed_roles=['Teacher'])
def teacher_page(request, pk):
	teacher = Teacher.objects.get(id=pk)
	# print(teacher.class_grade)
	student = Student.objects.filter(school_name__name = teacher.school_name.name)
	# print(student)
	context = {'teacher':teacher, 'student': student}
	
	return render(request, 'teacher-page.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['School Administrator'])
def administrator_page(request, pk):
	school = School.objects.get(id=pk)
	student = Student.objects.filter(school_name__name=school.name)
	teacher = Teacher.objects.filter(school_name__name=school.name)
	exam = Exam.objects.filter(school_name__name=school.name)
	
	context = {'school':school, 'student':student, 'teacher':teacher, 'exam':exam}
	return render(request, 'Dashboard2.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['Super User'])
def super_user(request, pk):
	# print(request.user.id)
	user = User.objects.get(id=pk)
	all_user = User.objects.all().count()
	student = Student.objects.all().count()
	teacher = Teacher.objects.all().count()
	school = School.objects.all()
	
	context = {'school': school, 'user': user, 'student': student, 'teacher':teacher, 'all_user': all_user}
	return render(request, 'superuser.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['School Administrator'])
def register_teacher(request):
	page = 'Teacher'
	# get the school because when submitted, complicated b/c school name is in foreignkey
	school = School.objects.get(email=request.user)
	form = RegisterTeacher()

	if request.method=='POST':
		form = RegisterTeacher(request.POST)
		name = request.POST['name'] +' '+ request.POST['fname'] +' '+ request.POST['gname']

		if form.is_valid():
			submit = form.save(commit=False)
			submit.role = page
			submit.name = name
			submit.school_name = school
			submit.save()
			return redirect('administrator', request.user.id)
		else:
			messages.error(request, 'An error has occurred')
		
	context = {'form':form, 'page':page}
	return render(request, 'registration.html', context)

@login_required(login_url='login')
def register_student(request):
	page = 'Student'
	school = School.objects.get(email=request.user)
	form = RegisterStudent()
	if request.method=='POST':
		form = RegisterStudent(request.POST)
		name = request.POST['name'] +' '+ request.POST['fname'] +' '+ request.POST['gname']
		
		if form.is_valid():
			submit = form.save(commit=False)
			submit.role = page
			submit.name = name
			submit.school_name = school
			submit.save()
			return redirect('administrator', request.user.id)
		else:
			print(form.errors, '=-----------')
			messages.error(request, 'An error has occurred')

	context = {'form': form, 'page':page}
	return render(request, 'registration.html', context)


def register_school(request):
	if request.user.is_superuser:
		form = RegisterSchool()
		
		if request.method == 'POST':
			form = RegisterSchool(request.POST)
			if form.is_valid():
				submit = form.save(commit=False)
				submit.role = 'School Administrator'
				submit.save()
				return redirect('superuser', request.user.id)
			else:
				print(form.errors)
	else:
		return redirect('administrator', request.user.id)
	
	context  ={'form': form, 'grade':range(4)}
	return render(request, 'school-registration.html', context)

def upcoming_exam(request, pk):
	exam = Exam.objects.get(id=pk)
	context = {'exam': exam}
	return render(request, 'upcoming_exams.html', context)

def account_page(request, pk):
	user = User.objects.get(id=pk)
	page = user.role

	return render(request, 'account.html', {'user': user, 'page':page})

def edit_account_school(request, pk):
	page = 'school'
	school = School.objects.get(id=pk)
	# instance for pre-fill
	form = EditAccountSchool(instance = school)
	#
	if request.method == 'POST':
		form = EditAccountSchool(request.POST, instance=school)
		if form.is_valid():
			update = form.save(commit=False)
			print(update.class_grade)
			if request.user.role == 'School Administrator':
				for x in update.class_grade:
					if not Grade.objects.filter(school=school, grade=x).exists():
						g = Grade(school=school, grade=x)
						print(g)
						g.save()
			update.save()
		else:
			print(form.errors)
			messages.error(request, 'Error has occurred Please try again')
		return redirect('administrator', school.id)
		
	context = {'form':form, 'page':page}
	return render(request, 'edit account/edit_school_form.html', context)

@allowed_user(allowed_roles=['School Administrator'])
def profile_page(request, pk):
	user = User.objects.get(id=pk)
	score = Score.objects.filter(student_score=user)
	print(user)
	context = {'user':user, 'score':score}
	return render(request, 'Profile/student-profile.html', context)

def profile_page_school(request, pk):
	school = School.objects.get(id=pk)
	context = {'school':school}
	return render(request, 'Profile/administrator-profile.html', context)

@login_required(login_url='login')
def change_password(request):
	if request.method == 'POST':
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		
		if password1 == password2:
			new_pass = make_password(password1)
			request.user.password = new_pass
			request.user.save()
			messages.success(request, 'You have successfully reset your password')
			return redirect('login')
		
		else:
			messages.error(request, 'Please check your password')
			
	return render(request, 'change_password.html')

def login_page(request):
	if request.method == 'POST':
		user = authenticate(
			email=request.POST['email'],
			password=request.POST['password']
		)
		
		if user is not None:
			login(request, user)
			
			if user.role=='Super User':
				return redirect('superuser', user.id)
			elif user.role=='Teacher':
				return redirect('teacher', user.id)
			elif user.role=='School Administrator':
				# print(user.id)
				return redirect('administrator', user.id )
			else:
				messages.error(request, 'You are not allowed here for the time being:)')
		else:
			messages.error(request, 'Email or Password is incorrect')
			return redirect('login')
		
	return render(request, 'login1.html')

def redirect_httpresponse(url, content_type, status_code=None):
	response = HttpResponse(content_type=content_type)
	response['Content-Disposition'] = f'attachment; filename=nj.docx'
	if status_code is not None:
		response.status_code = status_code
	response['Location'] = url
	return response

def create_exam(request):
	school = School.objects.get(email=request.user.teacher.school_name)
	form = CreateExam()
	max_choose = 80
	max_truefalse_blank = 10
	
	if request.method=='POST':
		form = CreateExam(request.POST)
		print(request.POST)
		if form.is_valid():
			squashed = squash(request.POST)
			# print(request.POST['truefalse_answer4'], '----------')
			# print(request.POST['fillblank_answer'])
			submit = form.save(commit=False)
			submit.school_name = school
			# # Because of foreignkey this complicated
			# # print(request.user.teacher.subject)
			submit.subject = request.user.teacher.subject
			submit.teacher = request.user.teacher
			submit.unique_name = request.POST['unique_name']
			submit.start_time = request.POST['start_time']
			submit.end_time = request.POST['end_time']
			submit.fillblank_answer = squashed[1]
			submit.choose_answer = squashed[2]
			submit.truefalse_answer = squashed[0]
			submit.save()
			print(submit.id)
			
			name_img = request.POST['unique_name']
			# document = Document()
			generate_qrcode(submit.id).save(f'doc_qrcode/qrcode/{name_img}.png')
			doc = DocxTemplate('doc_qrcode/AS - updated.docx')
			
			context = {
				'subjectStr': 'Biology',
				'qrcodeimg': InlineImage(doc, f'doc_qrcode/qrcode/{name_img}.png')
			}
			
			doc.render(context)
			response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			response['Content-Disposition'] = f'attachment; filename={name_img}.docx'
			doc.save(response)
			messages.success(request, 'Exam amswer is successfully created')

			return response
			
		else:
			messages.error(request, form.errors)
	
	context = {'form': form, 'max_choose':range(max_choose), 'max_truefalse_blank':range(max_truefalse_blank)}
	return render(request, 'exam.html', context)

def logout_user(request):
	logout(request)
	return redirect('login')

def grade_class(request):
	school = School.objects.all()

	context = {'school':school}
	return render(request, 'grade_class.html', context)

def student_list(request, pk):
	school = School.objects.get(id=pk)
	student = Student.objects.filter(Q(school_name__name__contains=school.name) | Q())


	context = {'student': student}
	return render(request, 'student-list.html', context)

def teacher_list(request, pk):
	school = School.objects.get(id=pk)
	teacher = Teacher.objects.filter(school_name__name=school.name)
	
	context = {'teacher': teacher}
	return render(request, 'teacher-list.html', context)

def exam_list(request, pk):
	school = School.objects.get(id=pk)
	exam = Exam.objects.filter(school_name__name=school.name)
	
	context = {'exam': exam}
	return render(request, 'exam-list.html', context)

def exam_result(request, pk):
	teacher = Teacher.objects.get(id=pk)
	x = Teacher.objects.all()
	print(x)
	score = Score.objects.filter(subject__teacher=teacher)
	y = Score.objects.all()
	print(y, 'score')
	context = {'score': score}
	return render(request, 'exam-result.html', context)
