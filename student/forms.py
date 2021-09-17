from django.forms import forms,ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','password1','password2']
		exclude =['email']
class CustomerForm(ModelForm):
	class Meta:
		model = Student
		fields="__all__"
		exclude=['user','enroll_year','section']


class TeacherForm(ModelForm):
	class Meta:
		model = Teacher
		fields="__all__"
		exclude=['user']

class ArrangementForm(ModelForm):
	class Meta:
		model = TeacherArrangment
		fields="__all__"
