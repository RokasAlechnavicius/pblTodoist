from django.shortcuts import render
from todoist.api import TodoistAPI
import json
import os
from dateutil import parser
import unicodedata2
import subprocess

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
    api.sync()
    print(api)
    i = 0
    j = 0
    data = {}
    dataT = {}
    data = []
    dataT = []
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
    subprocess.Popen(command2)
    command3 = ['python','manage.py','loaddata','projects.json']
    subprocess.Popen(command3)
    command4 = ['python','manage.py','loaddata','tasks.json']
    subprocess.Popen(command4)
    args ={'user':request.user}
    return render(request,'accounts/profile.html',args)
