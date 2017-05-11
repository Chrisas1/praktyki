from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        return render(request, 'cal/index.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username,password=password)
    if user is not None:
        login_user(request, user)
        return render(request, 'cal/index.html')
    else:
        return render(request, 'cal/login.html', {'error': "Błędny login lub hasło."})

def log_out(request):
    logout(request)
    return render(request, 'cal/login.html', {'logged_out': "Zostałeś wylogowany"})

