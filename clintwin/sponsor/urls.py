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
    path('openapi2', schema_view),
    # Move to API app
    path('loaddata/', views.load_data, name='load_data'),
    path('dummy/', views.dummy, name='dummy'),
    path('trial_match/', views.calculate_trial_matches, name='trial_matches'),
    path('question_rank/', views.question_rank, name='question_rank'),
    path('question_flow/', views.question_flow, name='question_flow'),
    # Move to API app
    path('token/', views.get_token, name='token'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('register/', TemplateView.as_view(template_name='sponsor/register.html'), name='signup'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/logout/', auth_views.LogoutView.as_view(template_name= 'registration/logged_out.html'), name='LogOut'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('viewtrials', views.viewTrials, name='viewtrials'),

    path("clinicaltrial_list2", views.ClinicalTrialListView2.as_view(), name='clinicaltrial_list2'),
    # NEW: for clinicaltrial_list2
    path('trial_view', views.TrialView.as_view(), name='trial_view'),  # NEW: for clinicaltrial_list2

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
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login_success/', views.login_success, name='login_success'),
    re_path(r'^profile/(?P<pk>\d+)$', views.SponsorDetailView.as_view(), name='sponsordetail'),
    re_path(r'^trial/(?P<pk>\d+)$', views.TrialDetailView.as_view(), name='trialdetail'),
    re_path(r'^updateprofile/(?P<pk>\d+)$', views.SponsorUpdateView.as_view(), name='sponsorupdate'),
    re_path(r'^updatetrial/(?P<pk>\d+)$', views.TrialUpdateView.as_view(), name='trialupdate'),
    re_path(r'^deleteprofile/(?P<pk>\d+)$', views.DeleteSponsorView.as_view(), name='sponsordelete'),
    re_path(r'^deletetrial/(?P<pk>\d+)$', views.DeleteTrialView.as_view(), name='trialdelete'),
]
