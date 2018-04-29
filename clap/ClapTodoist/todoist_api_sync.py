#Import todoist, get token and sync ir pisk naxui su sita nesamone
from todoist.api import TodoistAPI
import json
import os
from dateutil import parser

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

def make_dir(input_stringP):

    dirpath = ('JsonArrays/' + input_stringP + '/tasks/')
    try:
        os.makedirs(dirpath)
    except FileExistsError:
        print('Directory {} already exists'.format(dirpath))
    else:
        print('Directory {} created'.format(dirpath))


api = TodoistAPI('3ca2e79e1e14ec7de944dd93cc910ba12a9ccb29')


# Retrieving all projects, syncing with todoist api
api.sync()

i = 0
j = 0
data = {}
dataT = {}
data = []
dataT = []
for item in api.state['projects']:
    pid = api.state['projects'][i]['id']
    print(api.state['projects'][i]['item_order'])
    data.append({
        'model': 'projektai.projektas',
        'pk': api.state['projects'][i]['id'],
        'fields': {
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
