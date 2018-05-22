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


api = TodoistAPI('nani')


# Retrieving all projects, syncing with todoist api

if api.sync():
	print("good sync")
else:
	print("bad sync")
	
print(api.state['user'])
if api.state['user'] == {}:
	print("none")
else:
	print('exists')
