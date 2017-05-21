from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import Project, Task
from .forms import AddTask


def calcualte_tasks(user, current_week, current_day, container):
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
        containerid = container
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
        current_week = timezone.now().isocalendar()[1]
        current_day = timezone.now().day
        container = "events"
        tasks = calcualte_tasks(request.user, current_week, current_day, container)
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
        if int(page) == 0:
            return redirect('cal:index')
        else:
            time = timezone.now() - datetime.timedelta(days=int(page))
            current_week = time.isocalendar()[1]
            current_day = time.day
            container = "events"
            tasks = calcualte_tasks(request.user, current_week, current_day, container)
            prev_page = int(page) + 1
            next_page = int(page) - 1
            return render(request, 'cal/prev.html', {'tasks': tasks, 'prev_page': prev_page, 'next_page': next_page })


def next(request, page):
    if not request.user.is_authenticated:
        return render(request, 'cal/login.html')
    else:
        if int(page) == 0:
            return redirect('cal:index')
        else:
            time = timezone.now() + datetime.timedelta(days=int(page))
            current_week = time.isocalendar()[1]
            current_day = time.day
            container = "events"
            tasks = calcualte_tasks(request.user, current_week, current_day, container)
            prev_page = int(page) - 1
            next_page = int(page) + 1
            return render(request, 'cal/next.html', {'tasks': tasks, 'prev_page': prev_page, 'next_page': next_page })


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