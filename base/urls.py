from django.urls import path
from . import views

urlpatterns = [
	path('teacher/<str:pk>/', views.teacher_page, name='teacher'),
	path('administrator/<str:pk>/', views.administrator_page, name='administrator'),
	path('superuser/<str:pk>/', views.super_user, name='superuser'),
	
	path('register-teacher', views.register_teacher, name='register-teacher'),
	path('register-students', views.register_student, name='register-student'),
	path('register-schools', views.register_school, name='register-school'),
	
	
	path('upcoming-exam/<str:pk>/', views.upcoming_exam, name='upcoming-exam'),
	path('create-exam', views.create_exam, name='create-exam'),
	path('student-list/<str:pk>/', views.student_list, name='student-list'),
	path('teacher-list/<str:pk>/', views.teacher_list, name='teacher-list'),
	path('exam-list/<str:pk>/', views.exam_list, name='exam-list'),
	
	path('account/<str:pk>/', views.account_page, name='account'),
	path('edit_account/<str:pk>/', views.edit_account_school, name='edit-school-account'),
	path('profile/<str:pk>/', views.profile_page, name='profile'),
	path('profile-school/<str:pk>/', views.profile_page_school, name='profile-school'),
	path('change-password', views.change_password, name='change-password'),
	
	path('', views.login_page, name='login' ),
	path('logout', views.logout_user, name='logout'),
	
]