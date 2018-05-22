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
from django.contrib.auth import login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from accounts.forms import EditProfileInformationForm
from .models import Collaborator, UserProfile
from django.views import generic
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from ratelimit.decorators import ratelimit


def automatic_syncing():
    useriu_tokenai = tasks.list_users_and_stuff()
    # print(useriu_tokenai)
    return useriu_tokenai

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class SettingView(LoginRequiredMixin,generic.DetailView):
    model = UserProfile
    template_name = 'accounts/settings.html'

class UserProfileUpdate(LoginRequiredMixin,UpdateView):
    model = UserProfile
    fields = ['full_name', 'email','old_versions_count', 'mobile_number']



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/projektai/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/userprofile_form.html', {
        'form': form
    })





@login_required(login_url = 'login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST' :
        profile_form = EditProfileInformationForm(data=request.POST,instance = request.user.userprofile)
        if profile_form.is_valid():
            apikey=profile_form.cleaned_data.get('token')
            api = TodoistAPI(apikey)
            if api.state['user'] == {}:
                profile_form = EditProfileInformationForm(instance=request.user.userprofile)
                args = {'profile_form': profile_form,'exists':0}
                return render(request, 'accounts/profileform.html', args)
            profile_form.save()
            syncTodoist(user.userprofile.token,user.userprofile)
            # resyncing(user.userprofile.token, user.userprofile)
            # i_am_check(user.userprofile.token)
            # syncTodoist(user.userprofile.token, user.userprofile)
            return redirect('/projektai/')
        else:
            print(profile_form.errors)

    else:
        profile_form = EditProfileInformationForm(instance = request.user.userprofile)
    args = {'profile_form':profile_form,'exists':1}
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
                                            item_order=project.item_order,
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
            # if task.task_parent_id is None:
            #     pass
            # else:
            #     parent = task.task_parent_id.task_id
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
                                   # task_parent_id=parent,
                                   item_order=task.item_order,
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

def i_am_check(token,old_versions_count):
    a=1
    # nani = SyncedStuff.objects.filter(token = token).order_by('sync_time')
    for synced in SyncedStuff.objects.filter(token = token).order_by('sync_time'):
        nani = SyncedStuff.objects.filter(token=token).order_by('sync_time')
        if len(nani)>old_versions_count:
            Old_Projektas.objects.filter(Project_token=token,when_deleted=synced.sync_time).delete()
            Old_Task.objects.filter(Task_token=token,when_deleted=synced.sync_time).delete()
            synced.delete()
            # print(len(nani))
            # print(old_versions_count)
            a=a+1

# def checking_limits(request):
#     user = request.user
#     i_am_check(user.userprofile.token)
#     return render(request,'accounts/checked.html')

def syncTodoist(token,profilis):
    # make_dir(token)
    # os.chdir(token)
    api = TodoistAPI(token)
    for project in Projektas.objects.filter(Project_token=token):
         for task in Task.objects.filter(task_project_id=project.Project_ID):
             task.delete()
         project.delete()

    api.sync()
    i = 0
    Collaborator.objects.filter(id = api.state['user']['id']).update(full_name=api.state['user']['full_name'],email=api.state['user']['email'])
    Collaborator.objects.get_or_create(id = api.state['user']['id'],full_name=api.state['user']['full_name'],email=api.state['user']['email'])
    for item in api.state['collaborators']:
        if api.state['collaborators'][i]['id'] != api.state['user']['id']:
            Collaborator.objects.filter(id=api.state['collaborators'][i]['id']).update(email=api.state['collaborators'][i]['email'],
                                                full_name=str(unicodedata2.normalize('NFKD', (api.state['collaborators'][i]['full_name'])).encode('ascii','ignore'))[2:-1])
            Collaborator.objects.get_or_create(id=api.state['collaborators'][i]['id'],
                                                email=api.state['collaborators'][i]['email'],
                                                full_name=str(unicodedata2.normalize('NFKD', (api.state['collaborators'][i]['full_name'])).encode('ascii','ignore'))[2:-1])
        i = i + 1


    i=0
    j = 0
    monkaS = []
    monkaT=[]
    for item in api.state['projects']:
        pid = api.state['projects'][i]['id']
        monkaS.append({
            'Project_ID': api.state['projects'][i]['id'],
            'Project_token':profilis,
            'Project_name': api.state['projects'][i]['name'],
            'Parent_id': api.state['projects'][i]['parent_id'],
            'Color': api.state['projects'][i]['color'],
            'Indent': api.state['projects'][i]['indent'],
            'item_order':api.state['projects'][i]['item_order'],
            'is_deleted': api.state['projects'][i]['is_deleted'],
            'is_archived': api.state['projects'][i]['is_archived'],
        })
        for task in api.state['items']:
            if api.state['projects'][i]['id'] == api.state['items'][j]['project_id']:
                monkaT.append({
                    'Task_id': api.state['items'][j]['id'],
                    'task_token':profilis,
                    'task_Content': api.state['items'][j]['content'],
                    'task_project_id': api.state['items'][j]['project_id'],
                    # 'task_parent_id': api.state['items'][j]['parent_id'],
                    'item_order':api.state['items'][j]['item_order'],
                    'task_priority': api.state['items'][j]['priority'],
                    'task_indent': api.state['items'][j]['indent'],
                    'task_date_added': datefix(api.state['items'][j]['date_added']),
                    'task_due_date_utc': datefix(api.state['items'][j]['due_date_utc']),
                    'task_uid': api.state['items'][j]['user_id'],
                    'task_responsible_uid': api.state['items'][j]['responsible_uid'],
                    'checked': api.state['items'][j]['checked'],
                    'in_history': api.state['items'][j]['in_history'],
                    'is_deleted': api.state['items'][j]['is_deleted'],
                })
            j=j+1
        j=0
        i=i+1

    monkaS.sort(key=lambda x:x['item_order'])
    for item in monkaS:
        if item['Parent_id'] is not None:
            parentas = Projektas.objects.get(Project_ID=item['Parent_id'])
        else:
            parentas = None
        Projektas.objects.create(Project_ID=item['Project_ID'],
                                Project_token=item['Project_token'],
                                Project_name=item['Project_name'],
                                Parent_id = parentas,
                                Color = item['Color'],
                                Indent = item['Indent'],
                                item_order=item['item_order'],
                                is_deleted = item['is_deleted'],
                                is_archived = item['is_archived']
                                )


    monkaT.sort(key=lambda x:(x['item_order']))
    for item in monkaT:

        # if item['task_parent_id'] is not None:
        #     task_parentas = Task.objects.get(task_id=item['task_parent_id'])
        # else:
        #     task_parentas= None
        if item['task_responsible_uid'] is not None:
            responsible = Collaborator.objects.get(id=item['task_responsible_uid'])
        else:
            responsible=None
        Task.objects.create(task_id=item['Task_id'],
                            task_token=item['task_token'],
                            task_Content=item['task_Content'],
                            task_project_id=Projektas.objects.get(Project_ID=item['task_project_id']),
                            # task_parent_id=task_parentas,
                            item_order=item['item_order'],
                            task_priority=item['task_priority'],
                            task_indent=item['task_indent'],
                            task_date_added=item['task_date_added'],
                            task_due_date_utc=item['task_due_date_utc'],
                            task_uid=Collaborator.objects.get(id=item['task_uid']),
                            task_responsible_uid=responsible,
                            checked = item['checked'],
                            in_history=item['in_history'],
                            is_deleted=item['is_deleted']
                            )



    # command = ['cd']
    # subprocess.Popen(command)
    # os.system("python manage.py loaddata users/" + token + "/projects.json")
    # print("Projects sync started")
    #clap2 = subprocess.Popen(command3)
    #while clap2.poll() is None:
    # time.sleep(5)
    # print("projects sync done")
    # command4 = ['python','manage.py','loaddata','users/' + token +'/tasks.json']
    # os.system("python manage.py loaddata users/" + token + "/tasks.json")
    # print("Task sync started")
    #clap3 = subprocess.Popen(command4)
    #while clap3.poll() is None:


    # print('we did it reddit')

@ratelimit(key='ip',rate='1/m',method=ratelimit.ALL,block=True)
@login_required(login_url = 'login')
def resync(request):
    print(request.META['REMOTE_ADDR'])
    user = request.user
    # file = open('kek.txt','w')
    resyncing(user.userprofile.token,user.userprofile)
    i_am_check(user.userprofile.token,user.userprofile.old_versions_count)
    syncTodoist(user.userprofile.token,user.userprofile)
    return redirect('/projektai/')

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
@login_required(login_url = 'login')
def profile(request):
    # useriu_tokenai = automatic_syncing()
    # print(useriu_tokenai)
    user = request.user
    if user.userprofile.token is None:

        return edit_profile(request)
    else:
        # syncTodoist(user.userprofile.token)
    # print("Tasks sync is Done")
        return redirect('/projektai/')
        # args ={'user':request.user}
        # return render(request,'test.html',args)
        #return IndexView.as_view(request)
