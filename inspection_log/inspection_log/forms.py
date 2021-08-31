from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
        	'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        	'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
        	'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        	'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        	'password2': forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
        }
