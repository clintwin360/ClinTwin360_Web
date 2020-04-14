from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
schema_view = get_swagger_view(title='Pastebin API')


router = routers.DefaultRouter()
router.register(r'questions', views.ParticipantQuestionViewSet)
router.register(r'criteria', views.ClinicalTrialCriteraViewSet, basename='ClinicalTrialCriteria')
router.register(r'participants', views.ParticipantViewSet)
router.register(r'health', views.ParticipantBasicHealthViewSet)
router.register(r'responses', views.ParticipantResponseViewSet)
router.register(r'profile', views.SponsorProfileViewSet)
router.register(r'matches', views.ClinicalTrialMatchViewSet, basename='ClinicalTrialMatch')
router.register(r'trials', views.ClinicalTrialViewSet, basename='ClinicalTrial')

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('', include(router.urls)),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
]
