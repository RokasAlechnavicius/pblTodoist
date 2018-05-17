from django.conf.urls import url, include
from accounts import views
from django.contrib.auth import views as auth_views
# from views import IndexView
app_name = 'accounts'

urlpatterns = [
    url(r'^profile/$', views.profile,name = 'profile'),
    url(r'^resync/$', views.resync,name = 'resync'),
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r'^editprofile/$', views.edit_profile,name = 'edit_profile'),
    url(r'^settings/(?P<pk>\d+)/$', views.SettingView.as_view(), name='settings'),
    url(r'^settings/(?P<pk>\d+)/update/$', views.UserProfileUpdate.as_view(), name = 'update-setting'),
    url(r'^settings/password/$', views.change_password, name='change_password'),

]
