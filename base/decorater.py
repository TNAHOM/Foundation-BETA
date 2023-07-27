from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.role=='Super User':
			return redirect('superuser')
		elif request.user.role=='Teacher':
			return redirect('teacher')
		elif request.user.role=='Student':
			return redirect('student')
		elif request.user.role=='School Administrator':
			return redirect('administrator')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def allowed_user(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			
			role = None
			if request.user.role:
				role = request.user.role
				
			if role in allowed_roles:
				return view_func(request, *args, **kwargs)
			
			else:
				if request.user.role=='Super User':
					return redirect('superuser', request.user.id)
				elif request.user.role=='Teacher':
					return redirect('teacher', request.user.id)
				elif request.user.role=='Student':
					return redirect('student', request.user.id)
				elif request.user.role=='School Administrator':
					return redirect('administrator', request.user.id)
				return redirect('login')
	
		return wrapper_func
	return decorator