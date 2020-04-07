from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', views.ParticipantQuestionViewSet)
router.register(r'participants', views.ParticipantViewSet)
router.register(r'health', views.ParticipantBasicHealthViewSet)
router.register(r'responses', views.ParticipantResponseViewSet)
router.register(r'profile', views.SponsorProfileViewSet)
router.register(r'matches', views.ClinicalTrialMatchViewSet, basename='ClinicalTrialMatch')
router.register(r'trial', views.ClinicalTrialDetailsViewSet, basename='ClinicalTrial')
router.register(r'trials', views.ClinicalTrialViewSet, basename='ClinicalTrial')

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('', include(router.urls)),
]
