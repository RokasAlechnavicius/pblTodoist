from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.
from projektai.models import Projektas,Task
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
        return Projektas.objects.filter(Project_token=self.request.user.userprofile.token)


    def get_context_data(self,**kwargs):
        context = super(KekView,self).get_context_data(**kwargs)
        context['tasks']=Task.objects.all()
        return context
