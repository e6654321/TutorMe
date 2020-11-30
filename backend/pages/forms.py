from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
#DataFlair

#form for all data in table

# class OrderCreate(forms.ModelForm):
# 	date_registered = forms.DateField(required=False)
# 	address = forms.CharField(required=False)
# 	contact_number = forms.CharField(required=False)
# 	email = forms.CharField(required=False)
# 	customer = forms.IntegerField(required=False)
# 	product = forms.IntegerField(required = False)
# 	quantity = forms.IntegerField(required = False)
# 	isDeleted = forms.BooleanField(required=False)

# 	class Meta:
# 		model = Order
# 		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']