from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
        	'username': forms.TextInput(attrs={'id': 'reglogin'}),
        	'first_name': forms.TextInput(attrs={'id': 'regfirstname'}),
        	'last_name': forms.TextInput(attrs={'id': 'reglastname'}),
        	'password1': forms.PasswordInput(attrs={'id': 'regpassword1'}),
        	'password2': forms.PasswordInput(attrs={'id': 'regpassword2'}),
        }
