from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Client(models.Model):
    """
    Client model.
    """
    name = models.CharField(max_length=40)

    def __str__(self):
            return self.name


class Project(models.Model):
    """
    Project model.
    """
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=8, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Task model.
    """
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    to_do_time = models.IntegerField()
    start = models.DateTimeField('Start time')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def week_number(self):
        """
        Return week number of task starting time.
        """
        return self.start.isocalendar()[1]
