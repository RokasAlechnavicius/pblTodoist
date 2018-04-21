from django.shortcuts import render
from django.views.generic.list import ListView
from .fusioncharts import FusionCharts
# Create your views here.
from projektai.models import Projektas,Task
import json


# Loading Data from a Static JSON String
# Example to create a Column 2D chart with the chart data passed in JSON string format.
# The `fc_json` method is defined to load chart data from a JSON string.
# **Step 1:** Create the FusionCharts object in a view action

def megakek(request):
    column2d = FusionCharts("column2d", "ex1", "600", "400", "chart-1", "json",
        """{
        "chart": {
            "caption": "Monthly Revenue for last year",
            "subCaption": "Harry\'s Supermart",
            "xAxisName": "Month",
            "yAxisName": "Revenues (In USD)",
            "numberPrefix": "$",
            "theme": "zune"
        },
        "data": [{
            "label": "Jan",
            "value": "420000"
        }, {
            "label": "Feb",
            "value": "810000"
        }, {
            "label": "Mar",
            "value": "720000"
        }, {
            "label": "Apr",
            "value": "550000"
        }, {
            "label": "May",
            "value": "910000"
        }, {
            "label": "Jun",
            "value": "510000"
        }, {
            "label": "Jul",
            "value": "680000"
        }, {
            "label": "Aug",
            "value": "620000"
        }, {
            "label": "Sep",
            "value": "610000"
        }, {
            "label": "Oct",
            "value": "490000"
        }, {
            "label": "Nov",
            "value": "900000"
        }, {
            "label": "Dec",
            "value": "730000"
        }]
    }""")

  # Alternatively, you can assign this string to a string variable in a separate JSON file and
  # pass the URL of that file to the `dataSource` parameter.

    return render(request, 'projektai/megakek.html', {'output': column2d.render()})
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
        context['labels'] = kek
        context['values'] = values
        context['Indents'] = ProjectIndents
        context['Xvalues'] = NumberIndents
        return context
