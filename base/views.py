from django.shortcuts import render, redirect
from .models import User, Exam, Score, Teacher, Student, School, ClassGrade, Reports
from django.contrib.auth.decorators import login_required
from .forms import CreateExam, EditAccountSchool, EditAccountTeacher
from django.contrib import messages
from .utilities import squash

from .utilities import squash, generate_qrcode
from django.db.models import Q
from .utilities import remove_stuff

from .decorater import allowed_user
from docxtpl import DocxTemplate, InlineImage
from django.http import HttpResponse
import csv


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
	teacher_grade = teacher.class_grade.all()
	student = Student.objects.filter(school_name__name = teacher.school_name.name).order_by('-class_grade__class_grade')
	classG = ClassGrade.objects.filter(school=teacher.school_name)
	exam = Exam.objects.filter(teacher=teacher)[:5]
	print(dir(teacher_grade))
	print(teacher_grade.fetch_all())
	stu_num = 0
	for stu in teacher_grade:
		for stu_len in classG:
			if stu_len == stu:
				stu_num+=1
	context = {'teacher':teacher, 'student': student, 'teacher_grade':teacher_grade,
	           'stu_num':stu_num, 'exam':exam}
	
	return render(request, 'teacher-page.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['School Administrator'])
def administrator_page(request, pk):
	school = School.objects.get(id=pk)
	student = Student.objects.filter(school_name__name=school.name)[:10]
	teacher = Teacher.objects.filter(school_name__name=school.name)
	exam = Exam.objects.filter(school_name__name=school.name)
	
	context = {'school':school, 'student':student, 'teacher':teacher, 'exam':exam}
	return render(request, 'Dashboard2.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['Super User'])
def super_user(request, pk):
	user = User.objects.get(id=pk)
	all_user = User.objects.all().count()
	student = Student.objects.all().count()
	teacher = Teacher.objects.all().count()
	school = School.objects.all()
	reports = Reports.objects.filter(seen=False)[:5]
	
	context = {'school': school, 'user': user, 'student': student, 'teacher':teacher, 'all_user': all_user,
	           'reports':reports}
	return render(request, 'superuser.html', context)

def account_page_school(request, pk):
	school = School.objects.get(id=pk)
	return render(request, 'account.html', {'school': school})

def account_page_teacher(request, pk):
	teacher = Teacher.objects.get(id=pk)
	return render(request, 'account.html', {'teacher': teacher})

@login_required(login_url='login')
def edit_account_school(request, pk):
	page='school'
	school = School.objects.get(id=pk)
	# instance for pre-fill
	form = EditAccountSchool(instance = school)
	#
	if request.method == 'POST':
		form = EditAccountSchool(request.POST, instance=school)
		# print(form)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile successfully edited !!' )
		else:
			print(form.errors)
			messages.error(request, 'Error has occurred Please try again')
		return redirect('account-school', school.id)
		
	context = {'form':form, 'page':page}
	return render(request, 'edit account/edit_school_form.html', context)


@login_required(login_url='login')
def edit_account_teacher(request, pk):
	page = 'teacher'
	teacher = Teacher.objects.get(id=pk)
	# instance for pre-fill
	form = EditAccountSchool(instance=teacher)

	if request.method=='POST':
		form = EditAccountTeacher(request.POST, instance=teacher)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile successfully edited !!')
		else:
			print(form.errors)
			messages.error(request, 'Error has occurred Please try again')
		return redirect('teacher', teacher.id)
	
	context = {'form': form, 'page': page}
	return render(request, 'edit account/edit_school_form.html', context)


def create_exam(request):
	teacher = Teacher.objects.get(id=request.user.id)
	print(teacher.class_grade.all())
	form = CreateExam()
	max_choose = 80
	max_truefalse_blank = 10
	
	if request.method=='POST':
		form = CreateExam(request.POST)
		if form.is_valid():
			squashed = squash(request.POST)
			submit = form.save(commit=False)
			submit.school_name = teacher.school_name
			submit.teacher = request.user.teacher
			submit.unique_name = request.POST['unique_name']
			submit.start_time = request.POST['start_time']
			submit.fillblank_answer = squashed[1]
			submit.choose_answer = squashed[2]
			submit.truefalse_answer = squashed[0]
			submit.save()
			
			name_img = request.POST['unique_name']
			generate_qrcode(submit.id).save(f'doc_qrcode/qrcode/{name_img}.png')
			doc = DocxTemplate('doc_qrcode/AS - updated.docx')
			
			context = {
				'subjectStr': teacher.subject,
				'qrcodeimg': InlineImage(doc, f'doc_qrcode/qrcode/{name_img}.png'),
				'class': request.POST['class']
			}
			
			doc.render(context)
			response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			response['Content-Disposition'] = f'attachment; filename={name_img}.docx'
			doc.save(response)
			messages.success(request, 'Exam amswer is successfully created')

			return response
			
		else:
			messages.error(request, form.errors)
	
	context = {'teacher':teacher, 'form': form, 'max_choose':range(max_choose), 'max_truefalse_blank':range(max_truefalse_blank)}
	return render(request, 'exam.html', context)

def student_list_school(request, pk):
	page = 'school'
	school = School.objects.get(id=pk)
	student = Student.objects.filter(Q(school_name__name__contains=school.name) | Q())
	context = {'student': student, 'page':page}
	return render(request, 'student-list.html', context)

def student_list_teacher(request, pk):
	page = 'teacher'
	teacher = Teacher.objects.get(id=pk)
	teacher_grade = teacher.class_grade.all()
	student = Student.objects.filter(school_name=teacher.school_name).order_by('class_grade__class_grade')
	score = Score.objects.filter(student_score__school_name=teacher.school_name, subject__teacher=teacher)
	exam = Exam.objects.filter(school_name=teacher.school_name, teacher=teacher)
	# for x in exam:
	# 	y = x.score_set.all()
	# 	print(y)
	context = {'student': student, 'teacher_grade': teacher_grade,
	           'page':page, 'exam':exam, 'score':score}
	return render(request, 'student-list.html', context)

def teacher_list(request, pk):
	school = School.objects.get(id=pk)
	teacher = Teacher.objects.filter(school_name__name=school.name)
	grade = ClassGrade.objects.filter(school=school)
	# for x in grade:
	# 	# print(x)
	# 	print(x.teacher_set.all())

	
	context = {'teacher': teacher, 'grade': grade}
	return render(request, 'teacher-list.html', context)

def exam_list(request, pk):
	school = School.objects.get(id=pk)
	exam = Exam.objects.filter(school_name__name=school.name)
	
	context = {'exam': exam}
	return render(request, 'exam-list.html', context)

def exam_result(request, pk):
	teacher = Teacher.objects.get(id=pk)
	teacher_grade = teacher.class_grade.all()
	exam_name = Exam.objects.filter(teacher=teacher)
	score = Score.objects.filter(subject__teacher=teacher)

	if request.method == 'POST':
		print(request.POST)
		unique_name = request.POST["unique_name"]
		class_grade = request.POST['class_grade']
		dwn_score = Score.objects.filter(subject__unique_name=unique_name, student_score__class_grade__id=class_grade)
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = f'attachment; filename={unique_name}.csv'

		writer = csv.writer(response)
		writer.writerow(['Name', 'Score', 'Grade', 'Section', 'Date', 'Unique Name'])

		for dwn in dwn_score:
			exam_date = dwn.finished.strftime("%m/%d/%Y")
			writer.writerow([dwn.student_score.name, dwn.score, dwn.student_score.class_grade.class_grade, dwn.student_score.class_grade.section, exam_date, dwn.subject.unique_name])
		return response
	context = {'score': score, 'teacher_grade':teacher_grade, 'exam_names': exam_name}
	return render(request, 'exam-result.html', context)

def exam_detail(request, pk):
	exam = Exam.objects.get(id=pk)
	choose_ans = remove_stuff(exam.choose_answer, "',[] ")
	# print(exam.truefalse_answer.split())
	tf_ans = remove_stuff(exam.truefalse_answer, "',[]").split()
	fill_ans = remove_stuff(exam.fillblank_answer, "',[]").split()

	context = {'exam': exam, 'choose_ans': choose_ans, 'tf_ans': tf_ans,
	           'fill_ans': fill_ans}
	return render(request, 'exam-history.html', context)

def upcoming_exam(request):
	exam = Exam.objects.filter(teacher=request.user.id)
	context = {'exam': exam}
	return render(request, 'upcoming_exams.html', context)

def report_list(request):
	reports = Reports.objects.filter(seen=False)
	if request.method == 'POST':
		print(request.POST)
		submit = Reports.objects.get(id=request.POST['seen'])
		print(submit)
		submit.seen = True
		submit.save()
		print(submit)
		messages.success(request, f'Report removed from list({submit.user.name})')
	return render(request, 'report-list.html', {'reports': reports})
