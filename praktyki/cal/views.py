from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.utils import timezone
import datetime


def calcualte_tasks(user, current_week, current_day):
    user_tasks = user.task_set.all()
    user_week_tasks = [task for task in user_tasks if task.week_number() == current_week]
    user_today_tasks = [task for task in user_week_tasks if task.start.day == current_day]
    tasks_start = []
    tasks_end = []
    tasks_message = []
    tasks_description = []
    for task in user_today_tasks:
        start_time = timezone.localtime(task.start)
        start = (start_time.hour - 8) * 60 + start_time.minute
        end = start + task.to_do_time * 60
        message = task.name
        description = task.description
        tasks_start.append(start)
        tasks_end.append(end)
        tasks_message.append(message)
        tasks_description.append(description)
    tasks = zip(tasks_start, tasks_end, tasks_message, tasks_description)
    return tasks


def index(request):
    """
    View check if user is logged in, if not redirect to login page.
    """
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        current_week = timezone.now().isocalendar()[1]
        current_day = timezone.now().day
        tasks = calcualte_tasks(request.user, current_week, current_day)
        page_num = 0
        return render(request, 'cal/index.html', {'tasks': tasks, 'page_num': page_num})


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
        return redirect('cal:index')
    else:
        return render(request, 'cal/login.html', {'error': "Błędny login lub hasło."})


def log_out(request):
    """
    View logging out user.
    """
    logout(request)
    return render(request, 'cal/login.html', {'logged_out': "Zostałeś wylogowany"})


def previous(request, page):
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        time = timezone.now() - datetime.timedelta(days=int(page))
        current_week = time.isocalendar()[1]
        current_day = time.day
        tasks = calcualte_tasks(request.user, current_week, current_day)
        page_num = int(page)
        return render(request, 'cal/index.html', {'tasks': tasks, 'page_num': page_num})


def next(request, page):
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        time = timezone.now() + datetime.timedelta(days=int(page))
        current_week = time.isocalendar()[1]
        current_day = time.day
        tasks = calcualte_tasks(request.user, current_week, current_day)
        page_num = int(page)
        return render(request, 'cal/index.html', {'tasks': tasks, 'page_num': page_num })
