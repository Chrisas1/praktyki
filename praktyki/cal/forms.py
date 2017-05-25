from django import forms
from .models import Project
from django.contrib.auth.models import User
from django.utils import timezone

projects = Project.objects.all()
project_choices = [(x.name, x) for x in projects]
users = User.objects.all()
user_choices = [(x.username, x) for x in users]

class AddTask(forms.Form):
    name = forms.CharField(label='Task name', max_length=100)
    description = forms.CharField(label='Description', max_length=12, required=False)
    to_do_time = forms.IntegerField(label='To do time')
    start = forms.DateField(label='Day', input_formats=['%Y-%m-%d'], initial=timezone.now())
    project = forms.ChoiceField(label='Project', choices=project_choices)
    user = forms.ChoiceField(label='User', choices=user_choices)
    multiple_tasks = forms.IntegerField(label='Multiple Tasks', initial=1)