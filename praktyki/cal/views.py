from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User

def index(request):
    """
    View check if user is logged in, if not redirect to login page.
    """
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        return render(request, 'cal/index.html', {'logged_user': request.user})

def login(request):
    """
    Login view authenticate and login user.
    """
    user = None
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
    except Exception:
        print("No POST data")
    if user is not None:
        login_user(request, user)
        return render(request, 'cal/index.html')
    else:
        return render(request, 'cal/login.html', {'error': "Błędny login lub hasło."})

def log_out(request):
    """
    View logging out user.
    """
    logout(request)
    return render(request, 'cal/login.html', {'logged_out': "Zostałeś wylogowany"})

