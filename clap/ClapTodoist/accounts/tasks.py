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




@periodic_task(run_every=(crontab(minute='*/1')),name="task_do_a_sync")
def task_do_a_sync():
    users = User.objects.all()
    for user in users:
        if user.userprofile.token is not None:
            views.resyncing(user.userprofile.token, user.userprofile)
            views.i_am_check(user.userprofile.token)
            views.syncTodoist(user.userprofile.token, user.userprofile)

    return

# class AutomaticSyncronization(PeriodicTask):
#     run_every = timedelta(minutes = 5)
#
#     def run(self,**kwargs):
#         users = User.objects.all()
#         for user in users:
#             if user.userprofile.token is not None:
#                 views.resyncing(user.userprofile.token, user.userprofile)
#                 views.i_am_check(user.userprofile.token)
#                 views.syncTodoist(user.userprofile.token, user.userprofile)
#                 print('i did a sync')

@shared_task
def list_users_and_stuff():
    users = User.objects.all()
    vartotojai = []
    for user in users:
        if user.userprofile.token is not None:
            # print(user.userprofile.token)
            views.resyncing(user.userprofile.token, user.userprofile)
            views.i_am_check(user.userprofile.token)
            views.syncTodoist(user.userprofile.token, user.userprofile)
    return