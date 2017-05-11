from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=40)


class Project(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=8, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    to_do_time = models.IntegerField()
    start = models.DateField('Start time')
    end = models.DateField('End time')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)