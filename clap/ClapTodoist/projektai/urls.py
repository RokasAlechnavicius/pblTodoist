from django.conf.urls import url, include
from projektai import views
# from views import IndexView
app_name = 'projektai'

urlpatterns = [
url(r'^$',views.IndexView.as_view(),name='nani'),
url(r'^kek/$',views.KekView.as_view(),name='post_listas'),
url(r'^megakek/$',views.megakek,name = 'megakek'),
url(r'^alphadashboard/$',views.DashboardView.as_view(),name='dashboard'),
url(r'^table/$',views.smart,name='smar')

]
