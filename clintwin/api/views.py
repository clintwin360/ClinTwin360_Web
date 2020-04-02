##  Original additions
from django.http import HttpResponse
from requests import request, Response
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView

# Create your views here.
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer
