from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .fusioncharts import FusionCharts
# Create your views here.
from projektai.models import Projektas,Task,SyncedStuff,Old_Task,Old_Projektas
import json
from django.http import JsonResponse,HttpResponse
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def project_calculations(token,profile,projectinstance):
    data = []
    today= datetime.datetime.now().date()
    tommorow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tommorow, datetime.time())
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)
    this_month = datetime.datetime.now().month

    for project in Projektas.objects.filter(Project_token=token,Parent_id=None,Project_ID=projectinstance.Project_ID).order_by('item_order'):
        overdue = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
        tasks_today = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
        tasks_this_week = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
        tasks_this_month = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
        tasks_overall =  Task.objects.filter(task_project_id=project.Project_ID,task_token=token).count()
        own_tasks = Task.objects.filter(task_project_id=project.Project_ID,task_token=token).count()
        for subproject in Projektas.objects.filter(Project_token=token,Parent_id=project.Project_ID).order_by('item_order'):
            sub_overdue = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
            overdue=overdue+sub_overdue

            subtasks_today = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
            tasks_today=tasks_today+subtasks_today

            subtasks_this_week = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
            tasks_this_week=tasks_this_week+subtasks_this_week

            subtasks_this_month = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
            tasks_this_month=tasks_this_month + subtasks_this_month

            subown_tasks = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token).count()

            subtasks_overall =  Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token).count()
            tasks_overall = tasks_overall + subtasks_overall
            for subsubproject in Projektas.objects.filter(Project_token=token,Parent_id=subproject.Project_ID).order_by('item_order'):
                sub_sub_overdue = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
                overdue=overdue+sub_sub_overdue
                sub_overdue=sub_overdue+sub_sub_overdue

                subsubtasks_today = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
                tasks_today=tasks_today+subsubtasks_today
                subtasks_today=subtasks_today+subsubtasks_today

                subsubtasks_this_week = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
                tasks_this_week=tasks_this_week+subsubtasks_this_week
                subtasks_this_week=subtasks_this_week+subsubtasks_this_week

                subsubtasks_this_month = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
                tasks_this_month=tasks_this_month + subsubtasks_this_month
                subtasks_this_month = subtasks_this_month + subsubtasks_this_month

                subsubtasks_overall =  Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token).count()
                tasks_overall = tasks_overall + subsubtasks_overall
                subtasks_overall = subtasks_overall + subsubtasks_overall

                subsubown_tasks = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token).count()
                for subsubsubproject in Projektas.objects.filter(Project_token=token,Parent_id=subsubproject.Project_ID).order_by('item_order'):
                    sub_sub_sub_overdue = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
                    overdue=overdue+sub_sub_sub_overdue
                    sub_overdue=sub_overdue+sub_sub_sub_overdue
                    sub_sub_overdue=sub_sub_overdue+sub_sub_sub_overdue

                    subsubsubtasks_today = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
                    tasks_today=tasks_today+subsubsubtasks_today
                    subtasks_today = subtasks_today + subsubsubtasks_today
                    subsubtasks_today = subsubtasks_today + subsubsubtasks_today

                    subsubsubtasks_this_week = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
                    tasks_this_week=tasks_this_week+subsubsubtasks_this_week
                    subtasks_this_week=subtasks_this_week+subsubsubtasks_this_week
                    subsubtasks_this_week=subsubtasks_this_week + subsubsubtasks_this_week

                    subsubsubtasks_this_month = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
                    tasks_this_month=tasks_this_month + subsubsubtasks_this_month
                    subtasks_this_month = subtasks_this_month + subsubsubtasks_this_month
                    subsubtasks_this_month = subsubtasks_this_month + subsubsubtasks_this_month

                    subsubsubtasks_overall =  Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token).count()
                    tasks_overall = tasks_overall + subsubsubtasks_overall
                    subtasks_overall = subtasks_overall + subsubsubtasks_overall
                    subsubtasks_overall = subsubtasks_overall + subsubsubtasks_overall

                    subsubsubown_tasks = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token).count()

                    data.append({
                    "Project_name":"subsubsubproject " + subsubsubproject.Project_name,
                    'Project_ID':subsubsubproject.Project_ID,
                    "overdue":sub_sub_sub_overdue,
                    'item_order':subsubsubproject.item_order,
                    'tasks_today':subsubsubtasks_today,
                    'tasks_this_week':subsubsubtasks_this_week,
                    'tasks_this_month':subsubsubtasks_this_month,
                    "tasks_overall":subsubsubtasks_overall,
                    'project_indent':subsubsubproject.Indent,
                    'project_type':4,
                    'own_tasks':subsubsubown_tasks,
                    })

                data.append({
                "Project_name":"subsubproject " + subsubproject.Project_name,
                'Project_ID':subsubproject.Project_ID,
                "overdue":sub_sub_overdue,
                'item_order':subsubproject.item_order,
                'tasks_today':subsubtasks_today,
                'tasks_this_week':subsubtasks_this_week,
                'tasks_this_month':subsubtasks_this_month,
                "tasks_overall":subsubtasks_overall,
                'project_indent':subsubproject.Indent,
                'project_type':3,
                'own_tasks':subsubown_tasks,
                })

            data.append({
            "Project_name": "subproject " + subproject.Project_name,
            'Project_ID':subproject.Project_ID,
            "overdue":sub_overdue,
            'item_order':subproject.item_order,
            'tasks_today':subtasks_today,
            'tasks_this_week':subtasks_this_week,
            'tasks_this_month':subtasks_this_month,
            "tasks_overall":subtasks_overall,
            'project_indent':subproject.Indent,
            'project_type':2,
            'own_tasks':subown_tasks,
            })

        data.append({
        "Project_name":project.Project_name,
        'Project_ID':project.Project_ID,
        "overdue":overdue,
        'item_order':project.item_order,
        'tasks_today':tasks_today,
        'tasks_this_week':tasks_this_week,
        'tasks_this_month':tasks_this_month,
        "tasks_overall":tasks_overall,
        'project_indent':project.Indent,
        'project_type':1,
        'own_tasks':own_tasks,
        })
    data.sort(key=lambda x:x['item_order'])

    return data


def task_calculations(token,profile):
    tasks = Task.objects.filter(task_token = token)
    data = []
    today= datetime.datetime.now().date()
    tommorow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tommorow, datetime.time())
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)
    this_month = datetime.datetime.now().month
    for task in tasks:
        overdue=0
        task_today = 0
        task_this_week = 0
        task_this_month = 0
        overdue_query = Task.objects.filter(task_id=task.task_id,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=0).count()
        if overdue_query is not 0:
            overdue = 1
        if Task.objects.filter(task_id=task.task_id,task_due_date_utc__isnull=False,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=0).count() is not 0:
            task_today = 1
        if Task.objects.filter(task_id=task.task_id,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=0).count() is not 0:
            task_this_week = 1
        if Task.objects.filter(task_id=task.task_id,task_due_date_utc__month=this_month,checked=0).count() is not 0:
            task_this_month=1



        data.append({
        'task_Content':task.task_Content,
        'task_project_id':task.task_project_id,
        'overdue':overdue,
        'task_today':task_today,
        'task_this_week':task_this_week,
        'task_this_month':task_this_month,
        'checked':task.checked,
        'item_order':task.item_order
        })
    data.sort(key=lambda x:x['item_order'])
    return data


def big_calculations(token,profile):
    data = []
    today= datetime.datetime.now().date()
    tommorow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tommorow, datetime.time())
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)
    this_month = datetime.datetime.now().month

    for project in Projektas.objects.filter(Project_token=token,Parent_id=None).order_by('item_order'):
        overdue = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
        tasks_today = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
        tasks_this_week = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
        tasks_this_month = Task.objects.filter(task_project_id=project.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
        tasks_overall =  Task.objects.filter(task_project_id=project.Project_ID,task_token=token).count()
        for subproject in Projektas.objects.filter(Project_token=token,Parent_id=project.Project_ID).order_by('item_order'):
            sub_overdue = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
            overdue=overdue+sub_overdue

            subtasks_today = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
            tasks_today=tasks_today+subtasks_today

            subtasks_this_week = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
            tasks_this_week=tasks_this_week+subtasks_this_week

            subtasks_this_month = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
            tasks_this_month=tasks_this_month + subtasks_this_month

            subtasks_overall =  Task.objects.filter(task_project_id=subproject.Project_ID,task_token=token).count()
            tasks_overall = tasks_overall + subtasks_overall
            for subsubproject in Projektas.objects.filter(Project_token=token,Parent_id=subproject.Project_ID).order_by('item_order'):
                sub_sub_overdue = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
                overdue=overdue+sub_sub_overdue
                sub_overdue=sub_overdue+sub_sub_overdue

                subsubtasks_today = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
                tasks_today=tasks_today+subsubtasks_today
                subtasks_today=subtasks_today+subsubtasks_today

                subsubtasks_this_week = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
                tasks_this_week=tasks_this_week+subsubtasks_this_week
                subtasks_this_week=subtasks_this_week+subsubtasks_this_week

                subsubtasks_this_month = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
                tasks_this_month=tasks_this_month + subsubtasks_this_month
                subtasks_this_month = subtasks_this_month + subsubtasks_this_month

                subsubtasks_overall =  Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=token).count()
                tasks_overall = tasks_overall + subsubtasks_overall
                subtasks_overall = subtasks_overall + subsubtasks_overall
                for subsubsubproject in Projektas.objects.filter(Project_token=token,Parent_id=subsubproject.Project_ID).order_by('item_order'):
                    sub_sub_sub_overdue = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
                    overdue=overdue+sub_sub_sub_overdue
                    sub_overdue=sub_overdue+sub_sub_overdue
                    sub_sub_overdue=sub_sub_overdue+sub_sub_sub_overdue

                    subsubsubtasks_today = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
                    tasks_today=tasks_today+subsubsubtasks_today
                    subtasks_today = subtasks_today + subsubsubtasks_today
                    subsubtasks_today = subsubtasks_today + subsubsubtasks_today

                    subsubsubtasks_this_week = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
                    tasks_this_week=tasks_this_week+subsubsubtasks_this_week
                    subtasks_this_week=subtasks_this_week+subsubsubtasks_this_week
                    subsubtasks_this_week=subsubtasks_this_week + subsubsubtasks_this_week

                    subsubsubtasks_this_month = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token,task_due_date_utc__month=this_month,checked=False).count()
                    tasks_this_month=tasks_this_month + subsubsubtasks_this_month
                    subtasks_this_month = subtasks_this_month + subsubsubtasks_this_month
                    subsubtasks_this_month = subsubtasks_this_month + subsubsubtasks_this_month

                    subsubsubtasks_overall =  Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=token).count()
                    tasks_overall = tasks_overall + subsubsubtasks_overall
                    subtasks_overall = subtasks_overall + subsubsubtasks_overall
                    subsubtasks_overall = subsubtasks_overall + subsubsubtasks_overall

                    data.append({
                    "Project_name":"subsubsubproject " + subsubsubproject.Project_name,
                    'Project_ID':subsubsubproject.Project_ID,
                    "overdue":sub_sub_sub_overdue,
                    'item_order':subsubsubproject.item_order,
                    'tasks_today':subsubsubtasks_today,
                    'tasks_this_week':subsubsubtasks_this_week,
                    'tasks_this_month':subsubsubtasks_this_month,
                    "tasks_overall":subsubsubtasks_overall,
                    'project_indent':subsubsubproject.Indent,
                    'project_type':4,
                    })

                data.append({
                "Project_name":"subsubproject " + subsubproject.Project_name,
                'Project_ID':subsubproject.Project_ID,
                "overdue":sub_sub_overdue,
                'item_order':subsubproject.item_order,
                'tasks_today':subsubtasks_today,
                'tasks_this_week':subsubtasks_this_week,
                'tasks_this_month':subsubtasks_this_month,
                "tasks_overall":subsubtasks_overall,
                'project_indent':subsubproject.Indent,
                'project_type':3,
                })

            data.append({
            "Project_name": "subproject " + subproject.Project_name,
            'Project_ID':subproject.Project_ID,
            "overdue":sub_overdue,
            'item_order':subproject.item_order,
            'tasks_today':subtasks_today,
            'tasks_this_week':subtasks_this_week,
            'tasks_this_month':subtasks_this_month,
            "tasks_overall":subtasks_overall,
            'project_indent':subproject.Indent,
            'project_type':2,
            })

        data.append({
        "Project_name":project.Project_name,
        'Project_ID':project.Project_ID,
        "overdue":overdue,
        'item_order':project.item_order,
        'tasks_today':tasks_today,
        'tasks_this_week':tasks_this_week,
        'tasks_this_month':tasks_this_month,
        "tasks_overall":tasks_overall,
        'project_indent':project.Indent,
        'project_type':1,
        })
    data.sort(key=lambda x:x['item_order'])

    return data



def ProjectDashboard(request,pk=None):
    instance = get_object_or_404(Projektas,Project_ID=pk)
    project_data = project_calculations(request.user.userprofile.token,request.user.userprofile,instance)
    # print(project_data)
    tasks_data = task_calculations(request.user.userprofile.token,request.user.userprofile)
    # tasks_data.sort(key=lambda x:x['item_order'])
    checked_count = 0
    for task in tasks_data:
        if task['checked'] is 1:
            checked_count = checked_count + 1

    project_count = len(project_data)-1
    args={'clap':instance,'projects':project_data,'tasks':tasks_data,'project_count':project_count,'checked_count':checked_count,
    }
    # print(project_data[0]['tasks_overall'])

    return render(request,'projektai/projectpage.html',args)





def smart(request):
    data = big_calculations(request.user.userprofile.token,request.user.userprofile)
    # print(data)
    return render(request,'projektai/smart.html',{'data_json':data})
# Loading Data from a Static JSON String
# Example to create a Column 2D chart with the chart data passed in JSON string format.
# The `fc_json` method is defined to load chart data from a JSON string.
# **Step 1:** Create the FusionCharts object in a view action
@login_required(login_url = 'login')
def megakek(request):
    user = request.user
    all_events = Task.objects.filter(task_token=user.userprofile.token).exclude(task_due_date_utc__isnull=True,)
    for event in all_events:
        pass
    if request.GET:
        event_arr = []
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.task_Content
            start_date = datetime.datetime.strptime(str(i.task_date_added.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.task_due_date_utc.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))
    context = {
    'events':all_events
    }
    return render(request, 'projektai/megakek.html',context)
  # Alternatively, you can assign this string to a string variable in a separate JSON file and
  # pass the URL of that file to the `dataSource` parameter.

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'projektai/dashboard.html'

class IndexView(LoginRequiredMixin, ListView):
    context_object_name = 'post_list'
    template_name = 'projektai/index.html'

    def get_queryset(self):
        return Projektas.objects.filter(Project_token=self.request.user.userprofile.token,is_deleted=0).order_by('item_order')

    def get_context_data(self,**kwargs):
        big_data = big_calculations(self.request.user.userprofile.token,self.request.user.userprofile)
        context = super(IndexView,self).get_context_data(**kwargs)
        stuff = SyncedStuff.objects.filter(token = self.request.user.userprofile).order_by('-sync_time')
        skaicius = []
        for item in stuff:
            nania = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,when_deleted=item.sync_time).count()
            skaicius.append({
            'task_count':nania
            })
        context['crap'] = skaicius
        # context['old_sync'] = SyncedStuff.objects.filter(token = self.request.user.userprofile).order_by('-sync_time')
        context['last_synced_at'] = stuff[0].sync_time
        # synced_dates = []
        # for date in SyncedStuff.objects.filter(token = self.request.user.userprofile).order_by('-sync_time'):
        #     duomuo = date.sync_time
        #     synced_dates.append(duomuo.strftime('%m/%d/%Y'))
        # context['synced_dates']=synced_dates
        today= datetime.datetime.now().date()
        tommorow = today + datetime.timedelta(1)
        today_start = datetime.datetime.combine(today, datetime.time())
        today_end = datetime.datetime.combine(tommorow, datetime.time())
        context['data_json'] = big_data
        context['tasks'] = Task.objects.filter(task_token=self.request.user.userprofile.token)

        all_tasks = Task.objects.filter(task_token=self.request.user.userprofile.token).count()
        context['amount_tasks'] = all_tasks
        context['amount_projects'] = Projektas.objects.filter(Project_token=self.request.user.userprofile.token).count()
        checked_tasks = Task.objects.filter(task_token=self.request.user.userprofile.token,checked=1).count()
        context['amount_checked_tasks'] = checked_tasks
        context['amount_overdue_tasks'] = Task.objects.filter(task_token=self.request.user.userprofile.token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=0).count()
        context['amount_today_tasks'] = Task.objects.filter(task_token=self.request.user.userprofile.token,task_due_date_utc__isnull=False,checked=0,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start).count()
        overdue_projects = []
        for project in big_data:
            if project['overdue'] is not 0 and project['project_indent'] is 1:
                overdue_projects.append({
                'Project_name':project['Project_name'],
                'overdue':project['overdue'],
                'Project_ID':project['Project_ID']
                })
        context['overdue_projects'] = overdue_projects
        today_projects = []
        for project in big_data:
            if project['tasks_today'] is not 0 and project['project_indent'] is 1:
                today_projects.append({
                'Project_name':project['Project_name'],
                'tasks_count':project['tasks_today'],
                'Project_ID':project['Project_ID']
                })
        context['today_projects'] = today_projects
        if checked_tasks is not 0:
            floaterino = checked_tasks/all_tasks*100
            context['tasks_completed'] = int(floaterino)
        else:
            context['tasks_completed'] = 0
        current_time = datetime.datetime.now()
        timed_tasks = Task.objects.filter(task_token=self.request.user.userprofile.token,task_due_date_utc__lte=current_time,checked=0).count()
        timed_completed_tasks = Task.objects.filter(task_token=self.request.user.userprofile.token,task_due_date_utc__isnull=False).count()
        # print(timed_tasks)
        if timed_tasks is not 0:
            overdue_tasks = timed_tasks/all_tasks*100
            context['overdue']= int(overdue_tasks)
        else:
            context['overdue']= 0
        if timed_completed_tasks is not 0:
            overdue_completed_tasks = timed_completed_tasks/all_tasks*100
            context['deadline'] = int(overdue_completed_tasks)
        else:
            context['deadline'] = 0
        labels = []
        valuesComp = []
        valuesUcomp = []

        stuff = SyncedStuff.objects.filter(token=self.request.user.userprofile).order_by('-sync_time')
        values = []
        for item in stuff:
            ucompTaskCount = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,
                                                   when_deleted=item.sync_time, checked=0).count()

            compTaskCount = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,
                                                   when_deleted=item.sync_time, checked=1).count()

            date = item.sync_time
            date = date.strftime('%Y-%m-%d/%H:%M:%S')
            labels.append(date)

            valuesUcomp.append(ucompTaskCount)
            valuesComp.append(compTaskCount)

        context['labels'] = labels
        context['valuesComp'] = valuesComp
        context['valuesUcomp'] = valuesUcomp

        labelsdiff = []
        valuesdiff = []
        addedTasks = []
        deletedTasks = []
        completedTasks = []
        for item in stuff:
            oldTaskCount = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,
                                            when_deleted=item.sync_time).count()
            # values.append(oldTaskCount)
            # labels.append(str(item.sync_time))

        diff = SyncedStuff.objects.filter(token=self.request.user.userprofile).order_by('sync_time')
        syncs = []
        for item in diff:
            syncs.append(item.sync_time)
            # print(item.sync_time)

        difference = []
        count = 0
        i = 0
        for item in diff:
            addedTaskDiffList = []
            deletedTaskDiffList = []
            completedTaskDiffList = []
            tasksFirst = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,
                                            when_deleted=syncs[i]).order_by('task_id')
            tasksSecond = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,
                                            when_deleted=syncs[i+1]).order_by('task_id')

            for taskitem in tasksSecond:
                addedTaskDiffList.append(taskitem.task_Content)

            for taskitem in tasksFirst:
                deletedTaskDiffList.append(taskitem.task_Content)

            # j = 0
            for task in tasksSecond:
                for taskB4 in tasksFirst:
                    if task.task_id == taskB4.task_id:
                        addedTaskDiffList.remove(task.task_Content)

            for task in tasksSecond:
                for taskB4 in tasksFirst:
                    if task.task_id == taskB4.task_id:
                        deletedTaskDiffList.remove(task.task_Content)

            for task in tasksSecond:
                for taskB4 in tasksFirst:
                    if task.task_id == taskB4.task_id and task.checked == 1 and taskB4.checked == 0:
                        completedTaskDiffList.append(task.task_Content)

            if i < len(diff) - 2:
                i += 1


            # print(date, 'added', addedTaskDiffList, '---------- Count --  ',  len(addedTaskDiffList))
            # print(date, 'deleted', deletedTaskDiffList, '---------- Count --  ',  len(deletedTaskDiffList))
            # print(date, 'completed', completedTaskDiffList, '---------- Count --  ',  len(completedTaskDiffList))
            # print('Count of all changes - ', len(addedTaskDiffList)+len(deletedTaskDiffList)+len(completedTaskDiffList))
            # print()
            if len(addedTaskDiffList) > 0 or len(deletedTaskDiffList) > 0 or len(completedTaskDiffList) > 0:
                if len(addedTaskDiffList) > 0:
                    addedTasks.append(len(addedTaskDiffList))
                else:
                    addedTasks.append(0)

                if len(deletedTaskDiffList) > 0:
                    deletedTasks.append(len(deletedTaskDiffList))
                else:
                    deletedTasks.append(0)

                if len(completedTaskDiffList) > 0:
                    completedTasks.append(len(completedTaskDiffList))
                else:
                    completedTasks.append(0)

            if len(addedTaskDiffList) + len(deletedTaskDiffList) + len(completedTaskDiffList) > 0:
                date = syncs[i]
                date = date.strftime('%Y-%m-%d/%H:%M:%S')
                labelsdiff.append(date)

        context['addedTasks'] = addedTasks
        context['deletedTasks'] = deletedTasks
        context['completedTasks'] = completedTasks
        context['labelsdiff'] = labelsdiff
        context['valuesdiff'] = valuesdiff



        return context

#def index(request):
    #return render(request, 'accounts/index.html')




class KekView(LoginRequiredMixin, ListView):
    context_object_name = 'post_list'
    template_name = 'projektai/kek.html'
    queryset = Projektas.objects.all()

    def get_queryset(self):
        return Projektas.objects.filter(Project_token=self.request.user.userprofile.token,is_deleted=0).order_by('Project_ID')


    def get_context_data(self,**kwargs):
        context = super(KekView,self).get_context_data(**kwargs)
        context['tasks']=Task.objects.filter(is_deleted=0)
        ProjectIndents = []
        NumberIndents = []
        i=1
        a=0
        context['kekas']=len(Projektas.objects.filter(Project_token=self.request.user.userprofile.token,is_deleted=a))
        for projektas in Projektas.objects.filter(Project_token=self.request.user.userprofile.token):
            # print(projektas.Indent)
            ProjectIndents.append(projektas.Indent)
            NumberIndents.append(i)
            i=i+1

        labels = []
        values = []
        count = 0

        for project in Projektas.objects.filter(Project_token=self.request.user.userprofile.token):
            # labels.append(project.Project_name)
            for task in Task.objects.filter(task_project_id=project.Project_ID):
                # if project.Project_ID == task.task_project_id:
                count = count + 1

            if count != 0:
                values.append(count)
                name = project.Project_name
                # print(name)
                labels.append(name)
                # print(project.Project_name)
            # values.append(count)
            count = 0

        kek = labels
        # print(type(kek))
        # labels = json.dumps(kek)
        # print(labels)
        # labels = labels.replace('\"', 'QQQ')
        # print(labels)
        duomenys = {"labels":kek,"datasets":[{'data':values}]}
        context['stuff'] = duomenys

        context['labels'] = kek
        context['values'] = values
        context['Indents'] = ProjectIndents
        context['Xvalues'] = NumberIndents
        return context
