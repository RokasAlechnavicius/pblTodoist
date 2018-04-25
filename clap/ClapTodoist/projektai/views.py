from django.shortcuts import render
from django.views.generic.list import ListView
from .fusioncharts import FusionCharts
# Create your views here.
from projektai.models import Projektas,Task
import json
from django.http import JsonResponse,HttpResponse
import datetime



# Loading Data from a Static JSON String
# Example to create a Column 2D chart with the chart data passed in JSON string format.
# The `fc_json` method is defined to load chart data from a JSON string.
# **Step 1:** Create the FusionCharts object in a view action

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




class IndexView(ListView):
    context_object_name = 'post_list'
    template_name = 'projektai/index.html'
    queryset = Projektas.objects.all()

    def get_context_data(self,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['tasks']=Task.objects.order_by('task_priority')
        return context

class KekView(ListView):
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
