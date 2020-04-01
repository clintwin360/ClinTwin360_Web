from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

# Move to API app
router = routers.DefaultRouter()
router.register(r'questions', views.ParticipantQuestionViewSet)
router.register(r'participants', views.ParticipantViewSet)
router.register(r'responses', views.ParticipantResponseViewSet)

router.register(r'profile', views.SponsorProfileViewSet)
router.register(r'matches', views.ClinicalTrialMatchViewSet, basename='ClinicalTrialMatch')
router.register(r'trial', views.ClinicalTrialDetailsViewSet, basename='ClinicalTrial')


urlpatterns = [
    path('', views.index, name='index'),
    # Move to API app
    path('loaddata/', views.loaddata, name='loaddata'),
    path('dummy/', views.dummy, name='dummy'),
    # Move to API app
    path('token/', views.get_token, name='token'),
	path('accounts/', include('django.contrib.auth.urls')),
    path('register/', TemplateView.as_view(template_name='sponsor/register.html'), name='signup'),
	path('signup/', views.SignUp.as_view(), name='signup'),
    path('viewtrials', views.viewTrials, name='viewtrials'),
    path('newtrial', views.NewClinicalTrialView.as_view(), name='newtrial'),
    path('newtrial/inclusion', TemplateView.as_view(template_name='sponsor/inclusion.html'), name='inclusion'),
    path('newtrial/exclusion', TemplateView.as_view(template_name='sponsor/exclusion.html'), name='exclusion'),

    # path('newcriterion', TemplateView.as_view(template_name='sponsor/new_criterion.html'), name='new_criterion'),
    # path('viewcriteria', TemplateView.as_view(template_name='sponsor/view_criterian.html'), name='view_criteria'),
    path('newsponsor', views.NewSponsorView.as_view(), name='newsponsor'),
    path('viewsponsors', views.viewSponsors, name='viewsponsors'),
    path('viewsponsorreq', views.viewSponsorReq, name='viewsponsorreq'),

    path('about', views.AboutPageView.as_view(), name='about'),
    path('how_works', views.HowWorksPageView.as_view(), name='how_works'),
    path('contact', views.ContactPageView.as_view(), name='contact'),
    path('directions', views.DirectionsPageView.as_view(), name='directions'),
    path('contactform', views.contact, name='contactform'),
    # Move to API app
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login_success/', views.login_success, name='login_success'),
    re_path(r'^profile/<int:pk>/$', views.ProfileView.as_view(), name='profile'),
]
