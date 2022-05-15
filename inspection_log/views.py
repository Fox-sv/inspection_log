from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms
import json


def register_page(request):
    if request.user.is_authenticated:
        return redirect('inspection:start_page')
    else:
        form = forms.CreateUserForm()
        if request.method == "POST":
            form = forms.CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт ' + user + ' был создан ')
                return redirect('login')
            else:
                messages.info(request, 'Неверно введены данные')
        context = {'form': form}
        print(form.errors)
        return render(request, 'account/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('inspection:start_page')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inspection:start_page')
            else:
                messages.info(request, 'Неверный логин или пароль')
        context = {}
        return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('inspection:start_page')
