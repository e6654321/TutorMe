from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Details, Account
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CardDetailsForm(ModelForm):
    class Meta:
        model= Details
        fields = '__all__'

class AccountForm(ModelForm):
    class Meta:
        model= Account
        fields = '__all__'