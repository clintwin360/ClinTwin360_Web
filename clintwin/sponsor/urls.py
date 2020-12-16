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
    path('dashboard/', views.trial_dashboard, name='trial_dashboard'),
    # API Related Views
    path('loaddata/', views.load_data, name='load_data'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #Login/Password Views
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_success/', views.login_success, name='login_success'),
    #Trial Views
    re_path(r'^trial/(?P<pk>\d+)/criteria/inclusion/$', views.trial_criteria, {"criteria_type": "inclusion"}, name='inclusion_criteria'),
    re_path(r'^trial/(?P<pk>\d+)/criteria/exclusion/$', views.trial_criteria, {"criteria_type": "exclusion"}, name='exclusion_criteria'),
    re_path(r'^trial/(?P<pk>\d+)/criteria/review/$', views.review_criteria, name='review_criteria'),
    re_path(r'^updatetrial/(?P<pk>\d+)$', views.TrialUpdateView.as_view(), name='trialupdate'),
    path('newtrial', views.NewClinicalTrialView.as_view(), name='newtrial'),
    re_path(r'^trial/(?P<pk>\d+)/question_upload/$', views.question_upload, name='question_upload'),
    #Request Views
    path('viewsponsorreq', views.SponsorRequestListView.as_view(), name='viewsponsorreq'),
    path('criteriarequest', views.NewSponsorRequestView.as_view(), name='criteriarequest'),
    re_path(r'^criteriarequest/(?P<pk>\d+)$', views.SponsorRequestDetailView.as_view(), name='requestdetail'),
    path('contact', views.ContactPageView.as_view(), name='contact'),
    path('contactlist', views.ContactListView.as_view(), name='contactlist'),
    re_path(r'^contactrequest/(?P<pk>\d+)$', views.ContactDetailView.as_view(), name='contactdetail'),
    re_path(r'accessclose/(?P<pk>\d+)$', views.AccessRequestCloseView, name='accessclose'),
    re_path(r'criteriarequestcomplete/(?P<pk>\d+)$', views.CriteriaRequestCompleteView, name='criteriarequestcomplete'),
    re_path(r'requestnewsponsor/(?P<pk>\d+)$', views.NewSponsorFromRequest, name='newsponsorfromrequest'),
    #Sponsor Views
    path('newsponsor', views.NewSponsorView.as_view(), name='newsponsor'),
    path('newsponsorfill', views.NewSponsorFillView.as_view(), name='newsponsorfill'),
    path('viewsponsors', views.SponsorListView.as_view(), name='viewsponsors'),
    re_path(r'^profile/(?P<pk>\d+)$', views.SponsorDetailView.as_view(), name='sponsordetail'),
    re_path(r'^deleteprofile/(?P<pk>\d+)$', views.DeleteSponsorView.as_view(), name='sponsordelete'),
    re_path(r'^updateprofile/(?P<pk>\d+)$', views.SponsorUpdateView.as_view(), name='sponsorupdate'),
    #Account Views
    path('newaccount', views.NewAccountView.as_view(), name ='newaccount'),
    path('newaccountsponsoradmin', views.NewAccountSponsorAdminView.as_view(), name ='newaccountsponsoradmin'),
    path('accountfromsponsoradmin', views.NewAccountFromSponsorAdmin, name ='accountfromsponsoradmin'),
    path('passwordemail', views.PasswordEmailView, name='passwordemail'),
    re_path(r'accountfromsponsor/(?P<pk>\d+)$', views.NewAccountFromSponsor, name='accountfromsponsor'),
    re_path(r'user/(?P<pk>\d+)$', views.AccountDetailView.as_view(), name ='viewaccount'),
    # Supporting Views
    path('about', views.AboutPageView.as_view(), name='about'),
    path('how_works', views.HowWorksPageView.as_view(), name='how_works'),
]
