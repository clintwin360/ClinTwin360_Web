from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
schema_view = get_swagger_view(title='Pastebin API')


urlpatterns = [
    path('', views.index, name='index'),
    path('criteria_investigation/', views.criteria_investigation, name='criteria_investigation'),
    path('dummy/', views.dummy, name='dummy'),
    path('openapi2', schema_view),
    path('login_success/', views.login_success, name='login_success'),
    path('submit_criteria/', views.submit_criteria, name='submit_criteria'),
    # Move to API app
    path('loaddata/', views.load_data, name='load_data'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #Login/Password Views
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #Trial Views
    path('viewtrials', views.viewTrials, name='viewtrials'),
    re_path(r'^trial/(?P<pk>\d+)$', views.TrialDetailView.as_view(), name='trialdetail'),
    re_path(r'^pane/(?P<pk>\d+)$', views.TrialPaneView.as_view(), name='trialpane'),
    re_path(r'^updatetrialpane/(?P<pk>\d+)$', views.TrialUpdatePaneView.as_view(), name='trialupdatepane'),
    re_path(r'^updatetrial/(?P<pk>\d+)$', views.TrialUpdateView.as_view(), name='trialupdate'),
    re_path(r'^deletetrial/(?P<pk>\d+)$', views.DeleteTrialView.as_view(), name='trialdelete'),
    re_path(r'^deletetrialpane/(?P<pk>\d+)$', views.DeleteTrialPaneView.as_view(), name='trialdeletepane'),
	
	
    re_path(r'starttrial/(?P<pk>\d+)$', views.TrialStartView, name='trialstart'),#NEW
	re_path(r'endtrial/(?P<pk>\d+)$', views.TrialEndView, name='trialend'),#NEW
	
    path('newtrial', views.NewClinicalTrialView.as_view(), name='newtrial'),
    path('newtrial/inclusion', TemplateView.as_view(template_name='sponsor/inclusion.html'), name='inclusion'),
    path('newtrial/exclusion', TemplateView.as_view(template_name='sponsor/exclusion.html'), name='exclusion'),

    #For criteria
    path('newtrial/exclusion/addcriteria', views.NewEligibilityCriteriaView.as_view(), name='add_criteria'),

    #Sponsor Views
    path('newsponsor', views.NewSponsorView.as_view(), name='newsponsor'),
    path('viewsponsors', views.viewSponsors, name='viewsponsors'),
    path('viewsponsorreq', views.viewSponsorReq, name='viewsponsorreq'),
    re_path(r'^profile/(?P<pk>\d+)$', views.SponsorDetailView.as_view(), name='sponsordetail'),
    re_path(r'^deleteprofile/(?P<pk>\d+)$', views.DeleteSponsorView.as_view(), name='sponsordelete'),
    re_path(r'^updateprofile/(?P<pk>\d+)$', views.SponsorUpdateView.as_view(), name='sponsorupdate'),
    # Supporting Views
    path('about', views.AboutPageView.as_view(), name='about'),
    path('how_works', views.HowWorksPageView.as_view(), name='how_works'),
    path('contact', views.ContactPageView.as_view(), name='contact'),
    path('directions', views.DirectionsPageView.as_view(), name='directions'),
    path('emptypane', views.emptyPane, name='emptypane'),
]
