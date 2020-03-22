from django.shortcuts import render

##  Original additions
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from .models import User, UserManager, Contact
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
#from .forms import *
from django.views.generic.edit import FormView
from .forms import NewUserForm, UserCreationForm, NewTrialForm
#from .forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

# New additions

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import ClinicalTrial

# Create your views here.

# hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
#if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):

def index(request):
    return render(request, 'index.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'


"""
def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')


    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=request.POST['password'], email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})


def login(request):
    if (User.objects.filter(email=request.POST['login_email']).exists()):
        user = User.objects.filter(email=request.POST['login_email'])[0]
        if (request.POST['login_password'] == user.password):
            request.session['id'] = user.id
            return redirect('/success')
    return redirect('/')


def logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

"""
# View for contact us form
@api_view(['GET, POST'])
def contact(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = ContactForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('success.html')
    elif request.method == 'GET':
        # GET, generate unbound (blank) form
        form = ContactForm()
    return render(request,'contactform.html',{'form':form})

def newtrial(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = NewTrialForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('viewtrials.html')
    elif request.method == 'GET':
        # GET, generate unbound (blank) form
        form = NewTrialForm()
    return render(request,'newtrial.html',{'form':form})

def viewTrials(request):
    query_results = ClinicalTrial.objects.all()
    return render(request,"viewtrials.html")

"""
not working correctly.  need a django form?

@api_view(['GET', 'POST'])
def criteria(request):
    return render(request, 'criteria.html')
"""

# Static page for About us
class AboutPageView(TemplateView):
    template_name = 'about.html'

# Static page for How it Works
class HowWorksPageView(TemplateView):
    template_name = 'how_works.html'

# Static page for Contact us
class ContactPageView(TemplateView):
    template_name = 'contact.html'

# Static page for directions
class DirectionsPageView(TemplateView):
    template_name = 'directions.html'

# Static page for Message display
class MessagePageView(TemplateView):
    template_name = 'messages.html'

class NewTrialView(TemplateView):
    template_name = 'newtrial.html'

class TrialsView(TemplateView):
    template_name = 'viewtrials.html'

class CriteriaView(TemplateView):
    template_name = 'criteria.html'
