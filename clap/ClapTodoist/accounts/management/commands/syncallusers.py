from django.core.management.base import BaseCommand, CommandError
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from accounts import views

class Command(BaseCommand):
    help = 'resyncs the database n shit'

    def handle(self,*args,**options):
        users = User.objects.all()
        for user in users:
            if user.userprofile.token is not None:
                views.resyncing(user.userprofile.token, user.userprofile)
                views.i_am_check(user.userprofile.token)
                views.syncTodoist(user.userprofile.token, user.userprofile)

# self.stdout.write(self.style.SUCCESS('Successfully synced users'))