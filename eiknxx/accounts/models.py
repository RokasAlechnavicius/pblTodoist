from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import json
# Create your models here.

class Collaborator(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(blank=True,null=True)
    full_name = models.CharField(max_length=50,blank=True,null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userid = models.IntegerField(unique=True,blank=True,null=True)
    token = models.CharField(max_length=100,unique=True,blank=True,null=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    full_name = models.CharField(max_length=100,blank=True,null=True)
    inbox_project = models.IntegerField(blank=True,null=True)
    start_day = models.IntegerField(blank=True,null=True)
    next_week = models.IntegerField(blank=True,null=True)
    sort_order = models.IntegerField(blank=True,null=True)
    mobile_number = models.CharField(max_length=20,blank=True,null=True)
    mobile_host = models.CharField(max_length=50,blank=True,null=True)
    completed_count = models.IntegerField(blank=True,null=True)
    completed_today = models.IntegerField(blank=True,null=True)
    karma = models.IntegerField(blank=True,null=True)
    karma_trend = models.CharField(max_length=20,blank=True,null=True)
    is_premium = models.BooleanField(default=False)
    premium_until = models.CharField(max_length=100,blank=True,null=True)
    is_biz_admin = models.BooleanField(default=False)
    business_account_id = models.ForeignKey('self',to_field='id',blank=True,null=True,on_delete=models.PROTECT)
    join_date = models.DateTimeField(blank=True,null=True)




    def __str__(self):
        return self.token


def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile,sender=User)
