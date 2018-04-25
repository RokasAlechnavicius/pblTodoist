from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

class AboutPage(TemplateView):
    template_name = 'index.html'

class TestPage(LoginRequiredMixin,TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated==True:
            return HttpResponseRedirect(reverse("test"))
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("about"))
