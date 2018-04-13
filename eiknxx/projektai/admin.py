from django.contrib import admin
from .models import Task,Projektas, Old_Task,Old_Projektas
# Register your models here.
admin.site.register(Task)
admin.site.register(Projektas)
admin.site.register(Old_Task)
admin.site.register(Old_Projektas)
