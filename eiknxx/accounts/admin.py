from django.contrib import admin
from .models import UserProfile, Collaborator
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Collaborator)
