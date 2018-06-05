from django.conf.urls import url, include
from projektai import views
from . import views
# from views import IndexView
app_name = 'charts'

urlpatterns = [
    # url(r'^stacked/$', views.stackedCompUncompBar.as_view(), name='CompUncompTasks'),
    # url(r'^diff/$', views.dbDiff.as_view(), name='Database Differences'),

]
