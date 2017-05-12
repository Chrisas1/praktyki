from django.db import models
from django.contrib.auth.models import User
from cal.models import Task
from collections import Iterable


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hours_per_week = models.IntegerField()

    def tasks_hours(self, week_number):
        tasks = Task.objects.filter(user=self.user)
        week_tasks = [x for x in tasks if x.week_number() == week_number]
        tasks_hours = 0
        for task in week_tasks:
            tasks_hours += task.to_do_time
        return tasks_hours

    def available_hours(self, week_number):
        return self.hours_per_week - self.tasks_hours(week_number)