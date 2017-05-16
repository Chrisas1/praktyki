from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.
def week_sum(request):
    """
    Sends users data to template.
    """
    if request.user.is_authenticated:
        week_number = timezone.now().isocalendar()[1]
        users = User.objects.all()
        users_name_list = [x.username for x in users]
        users_tasks_hours_list = [x.worker.tasks_hours(week_number) for x in users]
        users_free_hours_list = [x.worker.available_hours(week_number) for x in users]
        users_info = zip(users_name_list, users_tasks_hours_list, users_free_hours_list)

        return render(request, 'week/index.html',{'users_info': users_info})

    else:
        return redirect('cal:index')