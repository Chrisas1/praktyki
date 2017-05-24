from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import Project, Task
from .forms import AddTask
from django.conf import settings

users_number = settings.USERS


def calcualte_tasks(user, current_week, current_day):
    user_tasks = user.task_set.all()
    user_week_tasks = [task for task in user_tasks if task.week_number() == current_week]
    user_today_tasks = [task for task in user_week_tasks if task.start.day == current_day]
    tasks_start = []
    tasks_end = []
    tasks_message = []
    tasks_description = []
    tasks_containerid = []
    for task in user_today_tasks:
        start_time = timezone.localtime(task.start)
        start = (start_time.hour - 8) * 60 + start_time.minute
        end = start + task.to_do_time * 60
        message = task.name
        description = task.description
        containerid = task.user.username
        tasks_start.append(start)
        tasks_end.append(end)
        tasks_message.append(message)
        tasks_description.append(description)
        tasks_containerid.append(containerid)
    tasks = zip(tasks_start, tasks_end, tasks_message, tasks_description, tasks_containerid)
    return tasks


def index(request):
    """
    View check if user is logged in, if not redirect to login page.
    """
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        kierownik = request.user.groups.filter(name="Kierownik").exists()
        current_week = timezone.now().isocalendar()[1]
        current_day = timezone.now().day
        tasks = calcualte_tasks(request.user, current_week, current_day)
        page_num = 0
        return render(request, 'cal/index.html', {'user': request.user, 'tasks': tasks, 'page_num': page_num, 'kierownik': kierownik})


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
        if int(page) == 0:
            return redirect('cal:index')
        else:
            kierownik = request.user.groups.filter(name="Kierownik").exists()
            time = timezone.now() - datetime.timedelta(days=int(page))
            current_week = time.isocalendar()[1]
            current_day = time.day
            tasks = calcualte_tasks(request.user, current_week, current_day)
            prev_page = int(page) + 1
            next_page = int(page) - 1
            return render(request, 'cal/prev.html', {'user': request.user, 'tasks': tasks, 'prev_page': prev_page, 'next_page': next_page, 'kierownik': kierownik })


def next(request, page):
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        if int(page) == 0:
            return redirect('cal:index')
        else:
            kierownik = request.user.groups.filter(name="Kierownik").exists()
            time = timezone.now() + datetime.timedelta(days=int(page))
            current_week = time.isocalendar()[1]
            current_day = time.day
            tasks = calcualte_tasks(request.user, current_week, current_day)
            prev_page = int(page) - 1
            next_page = int(page) + 1
            return render(request, 'cal/next.html', {'user': request.user, 'tasks': tasks, 'prev_page': prev_page, 'next_page': next_page, 'kierownik': kierownik })


def form(request):
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        if request.method == 'POST':
            taskform = AddTask(request.POST)
            if taskform.is_valid():
                for i in range(taskform.cleaned_data['multiple_tasks']):
                    name = taskform.cleaned_data['name']
                    description = taskform.cleaned_data['description']
                    to_do_time = taskform.cleaned_data['to_do_time']
                    start = taskform.cleaned_data['start'] + datetime.timedelta(days=i)
                    project = Project.objects.get(name=taskform.cleaned_data['project'])
                    user = User.objects.get(username=taskform.cleaned_data['user'])
                    Task.objects.create(name=name, 
                                        description=description,
                                        to_do_time=to_do_time,
                                        start=start,
                                        project=project,
                                        user=user)

                else:
                    pass
                return redirect('cal:form')
            else:
                return redirect('cal:form')
        else:
            taskform = AddTask()
            return render(request, 'cal/form.html', {'taskform': taskform})


def users(request, user_page):
    """
    View display all users stats.
    """
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        current_week = timezone.now().isocalendar()[1]
        current_day = timezone.now().day
        user_page = int(user_page)
        users = User.objects.all()[users_number * (user_page - 1):users_number * user_page]
        users_tasks = []
        for user in users:
            tasks = calcualte_tasks(user, current_week, current_day)
            users_tasks.append(tasks)
        if user_page > 1:
            prev_user_page = user_page - 1
        else:
            prev_user_page = 1
        user_pages = [prev_user_page, user_page, user_page + 1]
        kierownik = request.user.groups.filter(name="Kierownik").exists()
        return render(request, 'cal/users.html', {'users_tasks': users_tasks, 'users': users, 'user_pages': user_pages, 'kierownik': kierownik})


def next_users(request, page, user_page):
    """
    View display all users stats.
    """
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        if int(page) == 0:
            return redirect('cal:users', user_page)
        else:
            time = timezone.now() + datetime.timedelta(days=int(page))
            current_week = time.isocalendar()[1]
            current_day = time.day
            user_page = int(user_page)
            users = User.objects.all()[users_number * (user_page - 1):users_number * user_page]
            users_tasks = []
            for user in users:
                tasks = calcualte_tasks(user, current_week, current_day)
                users_tasks.append(tasks)
            page = int(page)
            pages = [page + 1, page, page - 1]
            if user_page > 1:
                prev_user_page = user_page - 1
            else:
                prev_user_page = 1
            user_pages = [prev_user_page, user_page, user_page + 1]
            kierownik = request.user.groups.filter(name="Kierownik").exists()
            return render(request, 'cal/next_users.html', {'users_tasks': users_tasks, 'users': users, 'pages': pages, 'user_pages': user_pages, 'kierownik': kierownik })


def prev_users(request, page, user_page):
    """
    View display all users stats.
    """
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        if int(page) == 0:
            return redirect('cal:users', user_page)
        else:
            time = timezone.now() - datetime.timedelta(days=int(page))
            current_week = time.isocalendar()[1]
            current_day = time.day
            user_page = int(user_page)
            users = User.objects.all()[users_number * (user_page - 1):users_number * user_page]
            users_tasks = []
            for user in users:
                tasks = calcualte_tasks(user, current_week, current_day)
                users_tasks.append(tasks)
            page = int(page)
            pages = [page - 1, page, page + 1]
            if user_page > 1:
                prev_user_page = user_page - 1
            else:
                prev_user_page = 1
            user_pages = [prev_user_page, user_page, user_page + 1]
            kierownik = request.user.groups.filter(name="Kierownik").exists()
            return render(request, 'cal/prev_users.html', {'users_tasks': users_tasks, 'users': users, 'pages': pages, 'user_pages': user_pages, 'kierownik': kierownik })