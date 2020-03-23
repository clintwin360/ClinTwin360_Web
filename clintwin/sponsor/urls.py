from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('viewtrials', views.viewTrials, name='viewtrials'),
    path('newtrial', TemplateView.as_view(template_name='sponsor/newtrial.html'), name='newtrial'),
    path('newtrial/criteria', TemplateView.as_view(template_name='sponsor/criteria.html'), name='criteria')
]
