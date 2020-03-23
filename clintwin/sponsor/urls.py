from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
	path('accounts/', include('django.contrib.auth.urls')),
    path('register/', TemplateView.as_view(template_name='sponsor/register.html'), name='signup'),
	path('signup/', views.SignUp.as_view(), name='signup'),
    path('viewtrials', views.viewTrials, name='viewtrials'),
    path('newtrial', TemplateView.as_view(template_name='sponsor/newtrial.html'), name='newtrial'),
    path('newtrial/criteria', TemplateView.as_view(template_name='sponsor/criteria.html'), name='criteria'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('how_works', views.HowWorksPageView.as_view(), name='how_works'),
    path('contact', views.ContactPageView.as_view(), name='contact'),
    path('directions', views.DirectionsPageView.as_view(), name='directions'),
    path('contactform', views.contact, name='contactform'),

]
