from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=40)


class Project(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=8, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    to_do_time = models.IntegerField()
    start = models.DateTimeField('Start time')
    end = models.DateTimeField('End time')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_continuous(self):
        if self.end - self.start <= datetime.timedelta(hours=self.to_do_time):
            return True
        else:
            return False

    def week_number(self):
        return self.start.isocalendar()[1]
