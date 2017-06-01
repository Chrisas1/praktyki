from django.db import models
from django.contrib.auth.models import User
from cal.models import Task
from collections import Iterable


class Worker(models.Model):
    """
    Model calculates not available hours and free hours.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hours_per_week = models.IntegerField()
    start_hour = models.IntegerField(default=8)
    max_hours = models.IntegerField(default=12)

    def tasks_hours(self, week_number):
        """
        Return how many hours are assigned. 
        """
        tasks = Task.objects.filter(user=self.user)
        week_tasks = [x for x in tasks if x.week_number() == week_number]
        tasks_hours = 0
        for task in week_tasks:
            tasks_hours += task.to_do_time
        return tasks_hours

    def available_hours(self, week_number):
        """
        Return free hours.
        """
        return self.hours_per_week - self.tasks_hours(week_number)
