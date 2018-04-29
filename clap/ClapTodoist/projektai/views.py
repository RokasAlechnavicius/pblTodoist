from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .fusioncharts import FusionCharts
# Create your views here.
from projektai.models import Projektas,Task,SyncedStuff
import json
from django.http import JsonResponse,HttpResponse
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required




def smart(request):
    data = []
    today= datetime.datetime.now().date()
    tommorow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tommorow, datetime.time())
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)
    this_month = datetime.datetime.now().month

    for project in Projektas.objects.filter(Project_token=request.user.userprofile.token,Parent_id=None).order_by('item_order'):
        overdue = Task.objects.filter(task_project_id=project.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
        tasks_today = Task.objects.filter(task_project_id=project.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
        tasks_this_week = Task.objects.filter(task_project_id=project.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
        tasks_this_month = Task.objects.filter(task_project_id=project.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__month=this_month,checked=False).count()
        tasks_overall =  Task.objects.filter(task_project_id=project.Project_ID,task_token=request.user.userprofile.token).count()
        for subproject in Projektas.objects.filter(Project_token=request.user.userprofile.token,Parent_id=project.Project_ID).order_by('item_order'):
            sub_overdue = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
            overdue=overdue+sub_overdue

            subtasks_today = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
            tasks_today=tasks_today+subtasks_today

            subtasks_this_week = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
            tasks_this_week=tasks_this_week+subtasks_this_week

            subtasks_this_month = Task.objects.filter(task_project_id=subproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__month=this_month,checked=False).count()
            tasks_this_month=tasks_this_month + subtasks_this_month

            subtasks_overall =  Task.objects.filter(task_project_id=subproject.Project_ID,task_token=request.user.userprofile.token).count()
            tasks_overall = tasks_overall + subtasks_overall
            for subsubproject in Projektas.objects.filter(Project_token=request.user.userprofile.token,Parent_id=subproject.Project_ID).order_by('item_order'):
                sub_sub_overdue = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
                overdue=overdue+sub_sub_overdue
                sub_overdue=sub_overdue+sub_sub_overdue

                subsubtasks_today = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
                tasks_today=tasks_today+subsubtasks_today
                subtasks_today=subtasks_today+subsubtasks_today

                subsubtasks_this_week = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
                tasks_this_week=tasks_this_week+subsubtasks_this_week
                subtasks_this_week=subtasks_this_week+subsubtasks_this_week

                subsubtasks_this_month = Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__month=this_month,checked=False).count()
                tasks_this_month=tasks_this_month + subsubtasks_this_month
                subtasks_this_month = subtasks_this_month + subsubtasks_this_month

                subsubtasks_overall =  Task.objects.filter(task_project_id=subsubproject.Project_ID,task_token=request.user.userprofile.token).count()
                tasks_overall = tasks_overall + subsubtasks_overall
                subtasks_overall = subtasks_overall + subsubtasks_overall
                for subsubsubproject in Projektas.objects.filter(Project_token=request.user.userprofile.token,Parent_id=subsubproject.Project_ID).order_by('item_order'):
                    sub_sub_sub_overdue = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__isnull=False,task_due_date_utc__lte=datetime.datetime.now(),checked=False).count()
                    overdue=overdue+sub_sub_sub_overdue
                    sub_overdue=sub_overdue+sub_sub_overdue
                    sub_sub_overdue=sub_sub_overdue+sub_sub_sub_overdue

                    subsubsubtasks_today = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=today_end,task_due_date_utc__gte=today_start,checked=False).count()
                    tasks_today=tasks_today+subsubsubtasks_today
                    subtasks_today = subtasks_today + subsubsubtasks_today
                    subsubtasks_today = subsubtasks_today + subsubsubtasks_today

                    subsubsubtasks_this_week = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__lte=this_week_end,task_due_date_utc__gte=this_week_start,checked=False).count()
                    tasks_this_week=tasks_this_week+subsubsubtasks_this_week
                    subtasks_this_week=subtasks_this_week+subsubsubtasks_this_week
                    subsubtasks_this_week=subsubtasks_this_week + subsubsubtasks_this_week

                    subsubsubtasks_this_month = Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=request.user.userprofile.token,task_due_date_utc__month=this_month,checked=False).count()
                    tasks_this_month=tasks_this_month + subsubsubtasks_this_month
                    subtasks_this_month = subtasks_this_month + subsubsubtasks_this_month
                    subsubtasks_this_month = subsubtasks_this_month + subsubsubtasks_this_month

                    subsubsubtasks_overall =  Task.objects.filter(task_project_id=subsubsubproject.Project_ID,task_token=request.user.userprofile.token).count()
                    tasks_overall = tasks_overall + subsubsubtasks_overall
                    subtasks_overall = subtasks_overall + subsubsubtasks_overall
                    subsubtasks_overall = subsubtasks_overall + subsubsubtasks_overall

                    data.append({
                    "Project_name":"                subsubsubproject " + subsubsubproject.Project_name,
                    "overdue":sub_sub_sub_overdue,
                    'item_order':subsubsubproject.item_order,
                    'tasks_today':subsubsubtasks_today,
                    'tasks_this_week':subsubsubtasks_this_week,
                    'tasks_this_month':subsubsubtasks_this_month,
                    "tasks_overall":subsubsubtasks_overall,
                    })

                data.append({
                "Project_name":"            subsubproject " + subsubproject.Project_name,
                "overdue":sub_sub_overdue,
                'item_order':subsubproject.item_order,
                'tasks_today':subsubtasks_today,
                'tasks_this_week':subsubtasks_this_week,
                'tasks_this_month':subsubtasks_this_month,
                "tasks_overall":subsubtasks_overall
                })

            data.append({
            "Project_name": "|____subproject " + subproject.Project_name,
            "overdue":sub_overdue,
            'item_order':subproject.item_order,
            'tasks_today':subtasks_today,
            'tasks_this_week':subtasks_this_week,
            'tasks_this_month':subtasks_this_month,
            "tasks_overall":subtasks_overall
            })

        data.append({
        "Project_name":"|__" + project.Project_name,
        "overdue":overdue,
        'item_order':project.item_order,
        'tasks_today':tasks_today,
        'tasks_this_week':tasks_this_week,
        'tasks_this_month':tasks_this_month,
        "tasks_overall":tasks_overall
        })
    data.sort(key=lambda x:x['item_order'])
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
        context = super(IndexView,self).get_context_data(**kwargs)
        context['old_sync'] = SyncedStuff.objects.filter(token = self.request.user.userprofile).order_by('-sync_time')
        synced_dates = []
        for date in SyncedStuff.objects.filter(token = self.request.user.userprofile).order_by('-sync_time'):
            duomuo = date.sync_time
            synced_dates.append(duomuo.strftime('%m/%d/%Y'))
        context['synced_dates']=synced_dates
        all_tasks = Task.objects.filter(task_token=self.request.user.userprofile.token).count()
        checked_tasks = Task.objects.filter(task_token=self.request.user.userprofile.token,checked=1).count()
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


        context['labels'] = labels
        context['values'] = values
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
