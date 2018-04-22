from django.conf.urls import url, include
from accounts import views
# from views import IndexView
app_name = 'accounts'

urlpatterns = [
    url(r'^profile/$', views.profile,name = 'profile'),
    url(r'^resync/$', views.resync,name = 'resync'),

]
