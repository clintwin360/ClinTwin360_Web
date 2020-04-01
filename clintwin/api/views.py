  ##  Original additions
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import TemplateView
#from .forms import *
from sponsor.forms import UserCreationForm, NewTrialForm
#from .forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import User, UserManager, Contact, Sponsor, Participant, ClinicalTrial, Criteria, Categories, ClinicalTrialCriteriaResponse, QuestionSchema, ParticipantQuestion

from rest_framework.decorators import api_view

# Create your views here.

