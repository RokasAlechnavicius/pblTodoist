from django.shortcuts import render,redirect
from todoist.api import TodoistAPI
import json
import os
from dateutil import parser
import unicodedata2
import subprocess
from projektai.models import Projektas,Task,Old_Task,Old_Projektas,SyncedStuff
from django.core import serializers
import time
import datetime
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import EditProfileInformationForm
from .models import Collaborator

from . import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

def make_dir(input_stringP):
    os.chdir('users')
    dirpath = (input_stringP)
    try:
        os.makedirs(dirpath)
    except FileExistsError:
        print('Directory {} already exists'.format(dirpath))
    else:
        print('Directory {} created'.format(dirpath))

def edit_profile(request):
    user = request.user
    if request.method == 'POST' :
        profile_form = EditProfileInformationForm(data=request.POST,instance = request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            syncTodoist(user.userprofile.token)
            return redirect('/projektai/')
        else:
            print(user_form.errors,profile_form.errors)

    else:
        profile_form = EditProfileInformationForm(instance = request.user.userprofile)
    args = {'profile_form':profile_form}
    return render(request,'accounts/profileform.html',args)



def resyncing(token,profilis):
    nani = Projektas.objects.filter(Project_token=token)
    time = datetime.datetime.now()
    for project in nani:
        if project.Parent_id is None:
            objektas = Old_Projektas.objects.create(Project_token=project.Project_token,
                                            Project_name=project.Project_name,
                                            Project_ID=project.Project_ID,
                                            Parent_id=None,
                                            Color=project.Color,
                                            Indent = project.Indent,
                                            is_deleted=project.is_deleted,
                                            is_archived=project.is_archived,
                                            when_deleted=time)

        else:
            objektas = Old_Projektas.objects.create(Project_token=project.Project_token,
                                                        Project_name=project.Project_name,
                                                        Project_ID=project.Project_ID,
                                                        Parent_id=project.Parent_id.Project_ID,
                                                        Color=project.Color,
                                                        Indent = project.Indent,
                                                        is_deleted=project.is_deleted,
                                                        is_archived=project.is_archived,
                                                        when_deleted=time)

    for project in Projektas.objects.filter(Project_token=token):
        for task in Task.objects.filter(task_project_id=project.Project_ID):
            parent = None
            tasko_resp_uid = None
            # file.write(str(task.task_project_id.Project_ID))
            # file.write(" newkek ")
            # file.write(str(task.task_uid.id))
            # file.write(" newkek ")
            if task.task_parent_id is None:
                pass
            else:
                parent = task.task_parent_id.task_id
                # file.write(str(parent))
                # print(parent)
            # file.write(' newkek ')
            if task.task_responsible_uid is None:
                pass
            else:
                # print("nani")
                tasko_resp_uid = task.task_responsible_uid.id
            #     file.write(str(tasko_resp_uid))
            #     print(tasko_resp_uid)
            # file.write("\n")

            taskas = Old_Task.objects.create(Task_token=profilis,
                                    task_Content=task.task_Content,
                                   task_id = task.task_id,
                                   task_project_id=task.task_project_id.Project_ID,
                                   task_parent_id=parent,
                                   task_priority=task.task_priority,
                                   task_indent=task.task_indent,
                                   task_date_added=task.task_date_added,
                                   task_due_date_utc = task.task_due_date_utc,
                                   task_uid = task.task_uid.id,
                                   task_responsible_uid=tasko_resp_uid,
                                   checked = task.checked,
                                   in_history = task.in_history,
                                   is_deleted = task.is_deleted,
                                   when_deleted=time
                                   )
    # file.close()
    syncas = SyncedStuff(token=profilis,
                        sync_time=time
                        )
    syncas.save()

    return

def i_am_check(token):
    a=1
    nani = SyncedStuff.objects.filter(token = token).order_by('sync_time')
    for synced in SyncedStuff.objects.filter(token = token).order_by('sync_time'):
        if a == 1 and len(nani)>4:
            Old_Projektas.objects.filter(Project_token=token,when_deleted=synced.sync_time).delete()
            Old_Task.objects.filter(Task_token=token,when_deleted=synced.sync_time).delete()
            synced.delete()
            a=a+1

# def checking_limits(request):
#     user = request.user
#     i_am_check(user.userprofile.token)
#     return render(request,'accounts/checked.html')

def create_old_models(token,user):
    # laikas = datetime.datetime.now()
    # print(user)
    a=0
    kappaset = Projektas.objects.filter(Project_token=user.userprofile.token)
    print(kappaset)
    for project in kappaset:
        print(project.Project_token)
        # print("kek")
        # print(project.Project_name)
        # objektas = Old_Projektas.objects.create(Project_token=project.Project_token,
        #                         Project_name=project.Project_name,
        #                         Project_ID=project.Project_ID,
        #                         Parent_id=project.Parent_id,
        #                         Color=project.Color,
        #                         Indent = project.Indent,
        #                         is_deleted=project.is_deleted,
        #                         is_archived=project.is_archived
        #                         )
        # print(objektas)
        # objektas.save()
        # a=a+1
        pass

    for project in Projektas.objects.filter(Project_token=token):
        for task in Task.objects.filter(task_project_id=project.Project_ID):
            # taskas = Old_Task(task_Content=task.task_Content,
            #                    task_id = task.task_id,
            #                    task_project_id=task.task_project_id,
            #                    task_parent_id=task.task_parent_id,
            #                    task_priority=task.task_priority,
            #                    task_indent=task.task_indent,
            #                    task_date_added=task.task_date_added,
            #                    task_due_date_utc = task.task_due_date_utc,
            #                    task_uid = task.task_uid,
            #                    task_responsible_uid=task.task_responsible_uid,
            #                    checked = task.checked,
            #                    in_history = task.in_history,
            #                    is_deleted = task.is_deleted
            #                    )
            # taskas.save()
            pass
    # print('Old stuff created ezpz')
    syncas = SyncedStuff(token=user.userprofile
                        )
    syncas.save()
    return

def syncTodoist(token):
    # Project_token = models.ForeignKey(UserProfile,to_field='token',on_delete=models.PROTECT,null=True)
    # Project_name = models.CharField(max_length=100)
    # Project_ID = models.IntegerField(null=True,blank=True)
    # Parent_id = models.ForeignKey(Projektas,to_field='Project_ID',null=True,blank=True,on_delete=models.CASCADE)
    # Color = models.IntegerField(null=True,blank=True)
    # Indent = models.IntegerField(null=True,blank=True)
    # is_deleted = models.IntegerField(null=True,blank=True)
    # is_archived = models.IntegerField(null=True,blank=True)
    # when_deleted =models.DateTimeField(default=datetime.datetime.now())
    make_dir(token)
    os.chdir(token)
    api = TodoistAPI(token)
    for project in Projektas.objects.filter(Project_token=token):
         for task in Task.objects.filter(task_project_id=project.Project_ID):
             task.delete()
         project.delete()

    api.sync()
    i = 0
    for item in api.state['collaborators']:
        Collaborator.objects.get_or_create(id=api.state['collaborators'][i]['id'],
                                            email=api.state['collaborators'][i]['email'],
                                            full_name=str(unicodedata2.normalize('NFKD', (api.state['collaborators'][i]['full_name'])).encode('ascii','ignore'))[2:-1])
        i = i + 1


    # print(api)
    i = 0
    j = 0
    data = {}
    dataT = {}
    data = []
    dataT = []
    # print(api.state['projects'])
    for item in api.state['projects']:
        pid = api.state['projects'][i]['id']
        data.append({
            'model': 'projektai.projektas',
            'pk': api.state['projects'][i]['id'],
            'fields': {
                'Project_token':token,
                'Project_name': api.state['projects'][i]['name'],
                'Parent_id': api.state['projects'][i]['parent_id'],
                'Color': api.state['projects'][i]['color'],
                'Indent': api.state['projects'][i]['indent'],
                'is_deleted': api.state['projects'][i]['is_deleted'],
                'is_archived': api.state['projects'][i]['is_archived'],
            }
        })

        for task in api.state['items']:
            if api.state['projects'][i]['id'] == api.state['items'][j]['project_id']:
                dataT.append({
                    'model': 'projektai.task',
                    'pk': api.state['items'][j]['id'],
                    'fields': {
                        'task_token':token,
                        'task_Content': api.state['items'][j]['content'],
                        'task_project_id': api.state['items'][j]['project_id'],
                        'task_parent_id': api.state['items'][j]['parent_id'],
                        'task_priority': api.state['items'][j]['priority'],
                        'task_indent': api.state['items'][j]['indent'],
                        'task_date_added': datefix(api.state['items'][j]['date_added']),
                        'task_due_date_utc': datefix(api.state['items'][j]['due_date_utc']),
                        'task_uid': api.state['items'][j]['user_id'],
                        'task_responsible_uid': api.state['items'][j]['responsible_uid'],
                        'checked': api.state['items'][j]['checked'],
                        'in_history': api.state['items'][j]['in_history'],
                        'is_deleted': api.state['items'][j]['is_deleted'],
                    }
                })

                with open('tasks.json', 'w') as fp:
                    json.dump(dataT, fp)

            j = j+1

        with open('projects.json', 'w') as fp:
            json.dump(data, fp)
        j = 0
        i = i + 1
    # command = ['cd']
    # subprocess.Popen(command)
    os.chdir('..')
    os.chdir('..')
    command3 = ['python','manage.py','loaddata','users/' + token +'/projects.json']
    # print("Projects sync started")
    clap2 = subprocess.Popen(command3)
    while clap2.poll() is None:
        time.sleep(2.5)
    # print("projects sync done")
    command4 = ['python','manage.py','loaddata','users/' + token +'/tasks.json']
    # print("Task sync started")
    clap3 = subprocess.Popen(command4)
    while clap3.poll() is None:
        time.sleep(0.5)


    # print('we did it reddit')



def resync(request):
    user = request.user
    # file = open('kek.txt','w')
    resyncing(user.userprofile.token,user.userprofile)
    i_am_check(user.userprofile.token)
    syncTodoist(user.userprofile.token)
    return redirect('/projektai/kek')

def decode(strC):
    newStr = str(unicodedata2.normalize('NFKD', strC.encode('ascii','ignore')))[2:-1]

def datefix(dt):

    if str(dt) == 'None':
        return None
    else:
        dt = str(dt)
        dt = parser.parse(dt)
        dt = str(dt)
        dt = dt[:-6]
        kek = dt[:10]
        kek = kek.__add__('T')
        kek2 = dt[11:]
        kek2 = kek2.__add__('Z')
        # print(kek)
        # print(kek2)
        kek = kek.__add__(kek2)
        # print(kek)
        return kek


# Create your views here.
def profile(request):
    user = request.user
    if user.userprofile.token is None:
        return edit_profile(request)
    else:
        # syncTodoist(user.userprofile.token)
    # print("Tasks sync is Done")
        args ={'user':request.user}
        return render(request,'projektai/index.html',args)
