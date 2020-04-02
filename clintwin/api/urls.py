from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
]