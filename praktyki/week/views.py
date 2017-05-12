from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def week_sum(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        users_name_list = [x.username for x in users]
        users_tasks_hours_list = [x.worker.tasks_hours(19) for x in users]
        users_free_hours_list = [x.worker.available_hours(19) for x in users]

        return render(request, 'week/index.html',{'users': users_name_list})

    else:
        return redirect('cal:index')