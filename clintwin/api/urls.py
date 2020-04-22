from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from sponsor.views import question_flow
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet

schema_view = get_swagger_view(title='Pastebin API')



router = routers.DefaultRouter()
router.register(r'questions', views.ParticipantQuestionViewSet)
router.register(r'criteria', views.ClinicalTrialCriteriaViewSet, basename='ClinicalTrialCriteria')
router.register(r'participants', views.ParticipantViewSet)
router.register(r'health', views.ParticipantBasicHealthViewSet)
router.register(r'responses', views.ParticipantResponseViewSet)
router.register(r'profile', views.SponsorProfileViewSet)
router.register(r'matches', views.ClinicalTrialMatchViewSet, basename='ClinicalTrialMatch')
router.register(r'trials', views.ClinicalTrialViewSet, basename='ClinicalTrial')
router.register(r'criteria_response', views.ClinicalTrialCriteriaResponseViewSet, basename='ClinicalTrialCriteriaResponse')
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    path('question_flow/', question_flow, name='question_flow'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('token/', views.get_token, name='token'),
    path('logout/', views.logout, name='api_logout'),
    path('', include(router.urls)),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
]
