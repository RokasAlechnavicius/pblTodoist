from django.shortcuts import render
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

    api = TodoistAPI(token)
    for project in Projektas.objects.filter(Project_token=token):
         for task in Task.objects.filter(task_project_id=project.Project_ID):
             task.delete()
         project.delete()

    api.sync()
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
    i = 0
    dataC = []
    for item in api.state['collaborators']:
        dataC.append({
            "model": "accounts.collaborator",
            "pk": api.state['collaborators'][i]['id'],
            "fields": {
                "email": api.state['collaborators'][i]['email'],
                "full_name": str(unicodedata2.normalize('NFKD', (api.state['collaborators'][i]['full_name'])).encode('ascii','ignore'))[2:-1]
            }})
        i = i + 1

        with open('collaborators.json', 'w') as fp:
            json.dump(dataC, fp)
    # command = ['cd']
    # subprocess.Popen(command)

    command2 = ['python','manage.py','loaddata','collaborators.json']
    # print("Collaborators sync started")
    clap =  subprocess.Popen(command2)
    while clap.poll() is None:
        time.sleep(1.5)
    # print("Collaborators synced")
    command3 = ['python','manage.py','loaddata','projects.json']
    # print("Projects sync started")
    clap2 = subprocess.Popen(command3)
    while clap2.poll() is None:
        time.sleep(1.5)
    # print("projects sync done")
    command4 = ['python','manage.py','loaddata','tasks.json']
    # print("Task sync started")
    clap3 = subprocess.Popen(command4)
    while clap3.poll() is None:
        time.sleep(2.5)


    # print('we did it reddit')



def resync(request):
    user = request.user
    nani = Projektas.objects.filter(Project_token=request.user.userprofile.token)
    # file = open('kek.txt','w')
    for project in nani:
        if project.Parent_id is None:
            objektas = Old_Projektas.objects.create(Project_token=project.Project_token,
                                            Project_name=project.Project_name,
                                            Project_ID=project.Project_ID,
                                            Parent_id=None,
                                            Color=project.Color,
                                            Indent = project.Indent,
                                            is_deleted=project.is_deleted,
                                            is_archived=project.is_archived)

        else:
            objektas = Old_Projektas.objects.create(Project_token=project.Project_token,
                                                        Project_name=project.Project_name,
                                                        Project_ID=project.Project_ID,
                                                        Parent_id=project.Parent_id.Project_ID,
                                                        Color=project.Color,
                                                        Indent = project.Indent,
                                                        is_deleted=project.is_deleted,
                                                        is_archived=project.is_archived)

    for project in Projektas.objects.filter(Project_token=request.user.userprofile.token):
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

            taskas = Old_Task.objects.create(task_Content=task.task_Content,
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
                                   is_deleted = task.is_deleted
                                   )
    # file.close()
    syncas = SyncedStuff(token=user.userprofile
                        )
    syncas.save()
    # print('done')
    # syncTodoist(token)

    return render(request,'accounts/success.html')

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
    api = TodoistAPI(user.userprofile.token)
    # print(user.userprofile.token)
    for project in Projektas.objects.filter(Project_token=user.userprofile.token):
         for task in Task.objects.filter(task_project_id=project.Project_ID):
             task.delete()
         project.delete()

    api.sync()
    print(api)
    i = 0
    j = 0
    data = {}
    dataT = {}
    data = []
    dataT = []
    print(api.state['projects'])
    for item in api.state['projects']:
        pid = api.state['projects'][i]['id']
        data.append({
            'model': 'projektai.projektas',
            'pk': api.state['projects'][i]['id'],
            'fields': {
                'Project_token':user.userprofile.token,
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
    #i = 0
    # dataU = []
    # dataU.append({
    #     "model": "accounts.userprofile",
    #     "pk": api.state['user']['id'],
    #     "fields": {
    #         "token": api.state['user']['token'],
    #         "email": api.state['user']['email'],
    #         "full_name": api.state['user']['full_name'],
    #         "inbox_project": api.state['user']['inbox_project'],
    #         "start_day": api.state['user']['start_day'],
    #         "next_week": api.state['user']['next_week'],
    #         "sort_order": api.state['user']['sort_order'],
    #         "mobile_number": api.state['user']['mobile_number'],
    #         "mobile_host": api.state['user']['mobile_host'],
    #         "completed_count": api.state['user']['completed_count'],
    #         "completed_today": api.state['user']['completed_today'],
    #         "karma": api.state['user']['karma'],
    #         "karma_trend": api.state['user']['karma_trend'],
    #         "is_premium": api.state['user']['is_premium'],
    #         "premium_until": api.state['user']['premium_until'],
    #         "is_biz_admin": api.state['user']['is_biz_admin'],
    #         "business_account_id": api.state['user']['business_account_id'],
    #         "join_date": datefix(api.state['user']['join_date']),
    #     }})
    #
    # with open('user.json', 'w') as fp:
    #     json.dump(dataU, fp)
    i = 0
    dataC = []
    for item in api.state['collaborators']:
        dataC.append({
            "model": "accounts.collaborator",
            "pk": api.state['collaborators'][i]['id'],
            "fields": {
                "email": api.state['collaborators'][i]['email'],
                "full_name": str(unicodedata2.normalize('NFKD', (api.state['collaborators'][i]['full_name'])).encode('ascii','ignore'))[2:-1]
            }})
        i = i + 1

        with open('collaborators.json', 'w') as fp:
            json.dump(dataC, fp)
    # command = ['cd']
    # subprocess.Popen(command)

    command2 = ['python','manage.py','loaddata','collaborators.json']
    # print("Collaborators sync started")
    clap =  subprocess.Popen(command2)
    while clap.poll() is None:
        time.sleep(0.5)
    # print("Collaborators synced")
    command3 = ['python','manage.py','loaddata','projects.json']
    # print("Projects sync started")
    clap2 = subprocess.Popen(command3)
    while clap2.poll() is None:
        time.sleep(0.5)
    # print("projects sync done")
    command4 = ['python','manage.py','loaddata','tasks.json']
    # print("Task sync started")
    clap3 = subprocess.Popen(command4)
    while clap3.poll() is None:
        time.sleep(0.5)


    # print("Tasks sync is Done")
    args ={'user':request.user}
    return render(request,'accounts/profile.html',args)
