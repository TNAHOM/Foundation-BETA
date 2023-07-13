from django.shortcuts import render, redirect
from .models import School, ClassGrade, Teacher, User, Reports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterTeacher, RegisterStudent, RegisterSchool
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .decorater import allowed_user


@login_required(login_url='login')
@allowed_user(allowed_roles=['School Administrator'])
def register_teacher(request):
	page = 'Teacher'
	# get the school because when submitted, complicated b/c school name is in foreignkey
	school = School.objects.get(email=request.user)
	form = RegisterTeacher()
	classGrade = ClassGrade.objects.filter(school=school).order_by('class_grade')
	classGrade2 = school.classgrade_set.all()
	
	if request.method=='POST':
		form = RegisterTeacher(request.POST)
		name = request.POST['name'] + ' ' + request.POST['fname'] + ' ' + request.POST['gname']

		print(form.errors)
		if form.is_valid():
			submit = form.save(commit=False)
			submit.role = page
			submit.name = name
			submit.school_name = school
			submit.save()
			
			teacher_name = Teacher.objects.get(email=submit)
			for x in request.POST.getlist('class_grade'):
				class_name = ClassGrade.objects.get(id=x)
				teacher_name.class_grade.add(class_name)

			return redirect('administrator', request.user.id)
		else:
			messages.error(request, 'An error has occurred')
	
	context = {'form': form, 'page': page, 'classGrade': classGrade, 'classGrade2': classGrade2}
	return render(request, 'registration.html', context)

@login_required(login_url='login')
def register_student(request):
	page = 'Student'
	school = School.objects.get(email=request.user)
	classGrade = ClassGrade.objects.filter(school=school).order_by('section')
	if request.method=='POST':
		form = RegisterStudent(request.POST)
		name = request.POST['name'] + ' ' + request.POST['fname'] + ' ' + request.POST['gname']
		add_classGrade = ClassGrade.objects.get(school=school, class_grade=request.POST['class_grade'],
			section=request.POST['section'])
		print(add_classGrade)
		if form.is_valid():
			submit = form.save(commit=False)
			submit.role = page
			submit.name = name
			submit.school_name = school
			submit.class_grade = add_classGrade
			print(submit.class_grade)
			submit.save()
			return redirect('administrator', request.user.id)
		else:
			print(form.errors, '=-----------')
			messages.error(request, 'An error has occurred')
	
	context = {'classGrade': classGrade, 'page': page}
	return render(request, 'registration.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['Super User'])
def register_school(request):
	if request.user.is_superuser:
		form = RegisterSchool()
		
		if request.method=='POST':
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
	
	context = {'form': form, 'grade': range(4)}
	return render(request, 'school-registration.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['School Administrator'])
def register_class(request, pk):
	school = School.objects.get(id=pk)
	if request.method=='POST':
		sections = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		for sec in range(int(request.POST.get('sec'))):
			ClassGrade.objects.get_or_create(school=school, class_grade=request.POST.get('class_grade'),
				section=sections[sec])
		return redirect('administrator', school.id)
	return render(request, 'register_class.html')

@login_required(login_url='login')
def change_password(request):
	if request.method=='POST':
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		
		if password1==password2:
			new_pass = make_password(password1)
			request.user.password = new_pass
			request.user.save()
			messages.success(request, 'You have successfully reset your password')
			return redirect('login')
		
		else:
			messages.error(request, 'Please check your password')
	
	return render(request, 'change_password.html')

def login_page(request):
	if request.method=='POST':
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
				return redirect('administrator', user.id)
			else:
				messages.error(request, 'You are not allowed here for the time being:)')
		else:
			messages.error(request, 'Email or Password is incorrect')
			return redirect('login')
	
	return render(request, 'login1.html')

def logout_user(request):
	logout(request)
	return redirect('login')

def report(request, pk):
	user = User.objects.get(id=pk)
	if request.method=='POST':
		# Report.objects.create(user=user, description=request.POST['report'].strip())
		form = Reports(user=user, description=request.POST['report'].strip(), seen=False)
		form.save()
		messages.success(request, 'Thank you for reporting your concern')
		if user.role == 'School Administrator':
			return redirect('administrator', user.id)
		elif user.role == 'Teacher':
			return redirect('teacher', user.id)

	return render(request, 'report.html')