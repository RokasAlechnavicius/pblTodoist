import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from accounts import views
from celery.task import PeriodicTask
from datetime import timedelta
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


def syncshit():
    users = User.objects.all()
    for user in users:
        if user.userprofile.token is not None:
            views.resyncing(user.userprofile.token, user.userprofile)
            views.i_am_check(user.userprofile.token)
            views.syncTodoist(user.userprofile.token, user.userprofile)
            print("sync done boi")