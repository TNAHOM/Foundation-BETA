from django.urls import path
from . import views
from . import reg_update

urlpatterns = [
	path('teacher/<str:pk>/', views.teacher_page, name='teacher'),
	path('administrator/<str:pk>/', views.administrator_page, name='administrator'),
	path('superuser/<str:pk>/', views.super_user, name='superuser'),
	
	path('register-teacher', reg_update.register_teacher, name='register-teacher'),
	path('register-students', reg_update.register_student, name='register-student'),
	path('register-schools', reg_update.register_school, name='register-school'),
	path('register-class/<str:pk>/', reg_update.register_class, name='register-class'),
	
	
	path('exam-detail/<str:pk>/', views.exam_detail, name='exam-detail'),
	path('upcoming-exam/', views.upcoming_exam, name='upcoming-exam'),
	path('create-exam', views.create_exam, name='create-exam'),
	path('student-lists/<str:pk>/', views.student_list_school, name='student-list-school'),
	path('student-list/<str:pk>/', views.student_list_teacher, name='student-list-teacher'),
	path('teacher-list/<str:pk>/', views.teacher_list, name='teacher-list'),
	path('exam-list/<str:pk>/', views.exam_list, name='exam-list'),
	path('exam-result/<str:pk>/', views.exam_result, name='exam-result'),
	
	path('account_school/<str:pk>/', views.account_page_school, name='account-school'),
	path('account_teacher/<str:pk>/', views.account_page_teacher, name='account-teacher'),
	path('edit_account_school/<str:pk>/', views.edit_account_school, name='edit-school-account'),
	path('edit_account_teacher/<str:pk>/', views.edit_account_teacher, name='edit-teacher-account'),
	path('change-password', reg_update.change_password, name='change-password'),
	
	path('report/<str:pk>/', reg_update.report, name='report'),
	path('report-list/', views.report_list, name='report-list'),
	path('', reg_update.login_page, name='login' ),
	path('logout', reg_update.logout_user, name='logout'),
	
]