from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'questions', views.ParticipantQuestionViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('loaddata/', views.loaddata, name='loaddata'),
	path('accounts/', include('django.contrib.auth.urls')),
    path('register/', TemplateView.as_view(template_name='sponsor/register.html'), name='signup'),
	path('signup/', views.SignUp.as_view(), name='signup'),
    path('viewtrials', views.viewTrials, name='viewtrials'),
    path('newtrial', TemplateView.as_view(template_name='sponsor/newtrial.html'), name='newtrial'),
    path('newtrial/inclusion', TemplateView.as_view(template_name='sponsor/inclusion.html'), name='inclusion'),
    path('newtrial/inclusion', TemplateView.as_view(template_name='sponsor/exclusion.html'), name='exclusion'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('how_works', views.HowWorksPageView.as_view(), name='how_works'),
    path('contact', views.ContactPageView.as_view(), name='contact'),
    path('directions', views.DirectionsPageView.as_view(), name='directions'),
    path('contactform', views.contact, name='contactform'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
