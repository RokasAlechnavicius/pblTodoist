from django.db import models
from accounts.models import UserProfile,Collaborator
import datetime
# Create your models here.
class Projektas(models.Model):
    Project_token = models.ForeignKey(UserProfile,to_field='token',on_delete=models.PROTECT,null=True)
    Project_name = models.CharField(max_length=100)
    Project_ID = models.BigIntegerField(primary_key=True)
    Parent_id = models.ForeignKey('self',to_field='Project_ID',null=True,blank=True,on_delete=models.CASCADE)
    Color = models.IntegerField(null=True,blank=True)
    Indent = models.IntegerField(null=True,blank=True)
    is_deleted = models.IntegerField(null=True,blank=True)
    is_archived = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return str(self.Project_name)

class Task(models.Model):
    task_Content = models.TextField(null=True,blank=True)
    task_id = models.BigIntegerField(primary_key=True)
    task_project_id = models.ForeignKey(Projektas,to_field='Project_ID',on_delete=models.CASCADE)
    task_parent_id = models.ForeignKey('self',to_field='task_id',null=True,blank=True,on_delete=models.CASCADE)
    task_priority = models.IntegerField(null=True,blank=True)
    task_indent = models.IntegerField(null=True,blank=True)
    task_date_added = models.DateTimeField(null=True,blank=True)
    task_due_date_utc = models.DateTimeField(null=True,blank=True)
    task_uid = models.ForeignKey(Collaborator,related_name='%(class)s_id',on_delete=models.CASCADE,null=True,blank=True)
    task_responsible_uid = models.ForeignKey(Collaborator,to_field='id',on_delete=models.CASCADE,null=True,blank=True)
    checked = models.IntegerField(null=True,blank=True)
    in_history = models.IntegerField(null=True,blank=True)
    is_deleted = models.IntegerField(null=True,blank=True)



class Old_Projektas(models.Model):
    Project_token = models.ForeignKey(UserProfile,to_field='token',on_delete=models.PROTECT,null=True)
    Project_name = models.CharField(max_length=100)
    Project_ID = models.IntegerField(null=True,blank=True)
    Parent_id = models.ForeignKey(Projektas,to_field='Project_ID',null=True,blank=True,on_delete=models.CASCADE)
    Color = models.IntegerField(null=True,blank=True)
    Indent = models.IntegerField(null=True,blank=True)
    is_deleted = models.IntegerField(null=True,blank=True)
    is_archived = models.IntegerField(null=True,blank=True)
    when_deleted =models.DateTimeField(default=datetime.datetime.now())

class Old_Task(models.Model):
    task_Content = models.TextField(null=True,blank=True)
    task_id = models.IntegerField()
    task_project_id = models.ForeignKey(Projektas,to_field='Project_ID',on_delete=models.CASCADE)
    task_parent_id = models.ForeignKey(Task,to_field='task_id',null=True,blank=True,on_delete=models.CASCADE)
    task_priority = models.IntegerField(null=True,blank=True)
    task_indent = models.IntegerField(null=True,blank=True)
    task_date_added = models.DateTimeField(null=True,blank=True)
    task_due_date_utc = models.DateTimeField(null=True,blank=True)
    task_uid = models.ForeignKey(Collaborator,related_name='%(class)s_id',on_delete=models.CASCADE,null=True,blank=True)
    task_responsible_uid = models.ForeignKey(Collaborator,to_field='id',on_delete=models.CASCADE,null=True,blank=True)
    checked = models.IntegerField(null=True,blank=True)
    in_history = models.IntegerField(null=True,blank=True)
    is_deleted = models.IntegerField(null=True,blank=True)
    when_deleted =models.DateTimeField(default=datetime.datetime.now())
