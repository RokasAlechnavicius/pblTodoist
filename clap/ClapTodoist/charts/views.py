from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.
from projektai.models import Projektas, Task, SyncedStuff, Old_Projektas, Old_Task
import json
import datetime

# Create your views here.
class stackedCompUncompBar(ListView):
    context_object_name = 'post_list'
    template_name = 'charts/histogram.html'
    queryset = Projektas.objects.all()

    def get_queryset(self):
        return Projektas.objects.filter(Project_token=self.request.user.userprofile.token)

    def get_context_data(self, **kwargs):
        context = super(stackedCompUncompBar, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
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
        return context

class dbDiff(ListView):
    context_object_name = 'post_list'
    template_name = 'charts/difference.html'
    queryset = Projektas.objects.all()

    def get_queryset(self):
        return Projektas.objects.filter(Project_token=self.request.user.userprofile.token)

    def get_context_data(self, **kwargs):
        context = super(dbDiff, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        labels = []
        values = []
        addedTasks = []
        deletedTasks = []
        completedTasks = []

        stuff = SyncedStuff.objects.filter(token=self.request.user.userprofile).order_by('-sync_time')
        values = []
        for item in stuff:
            oldTaskCount = Old_Task.objects.filter(Task_token=self.request.user.userprofile.token,
                                            when_deleted=item.sync_time).count()
            # values.append(oldTaskCount)
            # labels.append(str(item.sync_time))

        diff = SyncedStuff.objects.filter(token=self.request.user.userprofile).order_by('sync_time')
        syncs = []
        for item in diff:
            syncs.append(item.sync_time)
            print(item.sync_time)

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
                labels.append(date)



        context['addedTasks'] = addedTasks
        context['deletedTasks'] = deletedTasks
        context['completedTasks'] = completedTasks
        context['labels'] = labels
        context['values'] = values
        return context
