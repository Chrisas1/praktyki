from django.contrib import admin

from .models import Client, Project, Task, Day

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Day)