##  Original additions
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from django.views.generic import TemplateView
# from .forms import *
from sponsor.forms import UserCreationForm, NewTrialForm, NewSponsorForm
# from .forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics

# New additions

from rest_framework.decorators import api_view
from .models import User, UserManager, Contact, Sponsor, Participant, ClinicalTrial, ClinicalTrialCriteriaResponse, \
    ParticipantQuestion
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .serializers import *
from django.core.management import call_command
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import Count

# New
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import ClinicalTrialTable
from rest_framework import pagination


# Create your views here.


# hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
# if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('login_success')


def login_success(request):
    if request.user.groups.filter(name='clintwin'):
        return redirect("viewsponsors")
    else:
        return redirect("viewtrials")

#Trial Views
def viewTrials(request):
    trials = ClinicalTrial.objects.all()  # filter(sponsorId=request.user.sponsor_id)
    return render(request, "sponsor/viewtrials.html", {"trials": trials})

class TrialDetailView(generic.DetailView):
    model = ClinicalTrial

class TrialUpdateView(generic.UpdateView):
    model = ClinicalTrial
    fields = ['title']

#Sponsor Views

class SponsorDetailView(generic.DetailView):
    model = Sponsor

class SponsorUpdateView(generic.UpdateView):
    model = Sponsor
    fields = ['organization']

def dummy(request):
    questions = ParticipantQuestion.objects.all()
    return render(request, 'sponsor/dummy.html', {"questions": questions})


def get_token(request):
    x = get_user(request)
    token = Token.objects.create(user=x)
    return HttpResponse(token)


def compare_values(a, op, b):
    if op == "equals":
        return a == b
    if op == 'gte':
        return float(a) >= float(b)
    if op == 'lte':
        return float(a) <= float(b)


def calculate_trial_matches(request):
    participant = Participant.objects.get(id=1)
    responses = participant.responses.all()
    trials = ClinicalTrial.objects.all()
    data = {'matches': [], 'questions': []}
    for trial in trials:
        trial_match = True
        criteria = trial.criteria.all()
        for criterion in criteria:
            if trial_match:
                criterion_value = criterion.value
                comparison = criterion.comparison
                criterion_type = criterion.criteriaType
                question = criterion.criteria.question
                print(question.text)
                response = responses.get(question__id=question.id)
                response_value = response.value
                value_match = compare_values(response_value, comparison, criterion_value)
                data['questions'].append({'text': question.text, 'expected': criterion_value,
                                          'comparison': comparison, 'type': criterion_type,
                                          'response': response_value, 'status': value_match})
                if value_match and criterion_type == "inclusion" or not value_match and criterion_type == "exclusion":
                    continue
                else:  # this will not match if value_match is not true or if type is exclusion, we may want to separate cases
                    trial_match = False
                    continue
        if trial_match:
            data['matches'].append(trial.title)
    data['participant'] = participant.name()
    data['responses'] = [x.question.text for x in participant.responses.all()]
    return JsonResponse(data)


def question_rank(questions):
    ranks = {}
    for q in questions:
        rank = 0
        criteria = q.criteria.all()
        for criterion in criteria:
            rank += criterion.trial_responses.count()
        ranks[q.id] = rank

    #data['questions'].sort(key=lambda x: x['rank'], reverse=True)
    return ranks


def question_flow(request):
    questions = ParticipantQuestion.objects.all()
    ranks = question_rank(questions)
    data = {'questions': []}
    for question in questions:
        flow = question.question_flow.all()
        is_followup = QuestionFlow.objects.filter(next_question=question.id).count()
        data['questions'].append({'id': question.id,
                                  'text': question.text,
                                  'is_followup': is_followup,
                                  'rank': ranks[question.id],
                                  'value_type': question.valueType,
                                  'options':
                                      [{'value': x.response, 'next_question': x.next_question.id} for x in flow]})
    return JsonResponse(data)


def load_data(request):
    call_command('loaddata', 'participant_questions')
    call_command('loaddata', 'users')
    call_command('loaddata', 'participants')
    call_command('loaddata', 'trial_criteria')
    call_command('loaddata', 'sponsors')
    call_command('loaddata', 'clinical_trials')
    call_command('loaddata', 'criteria_responses')
    call_command('loaddata', 'trial_matches')
    call_command('loaddata', 'participant_responses')
    call_command('loaddata', 'question_flow')
    return HttpResponse("Data Loaded!")


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
    return render(request, 'contactform.html', {'form': form})


class ClinicalTrialCreateView(generic.CreateView):
    model = ClinicalTrial
    fields = (
        'id', 'sponsorId', 'title', 'objective', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget',
        'url',
        'followUp', 'location', 'comments')
    template_name = 'create_trial_form.html'


@api_view(['GET'])
class TrialList(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


"""
not working correctly.  need a django form?
@api_view(['GET', 'POST'])
def criteria(request):
    return render(request, 'criteria.html')
"""


def viewSponsors(request):
    queryset = Sponsor.objects.all()
    return render(request, "sponsor/view_sponsors.html")


def viewSponsorReq(request):
    query_results = SponsorRequest.objects.all()
    return render(request, "sponsor/view_sponsor_req.html")


# Static page for About us
class AboutPageView(TemplateView):
    template_name = 'sponsor/about.html'


# Static page for How it Works
class HowWorksPageView(TemplateView):
    template_name = 'sponsor/how_works.html'


# Static page for Contact us
class ContactPageView(TemplateView):
    template_name = 'sponsor/contact.html'


# Static page for directions
class DirectionsPageView(TemplateView):
    template_name = 'directions.html'


# Static page for Message display
class MessagePageView(TemplateView):
    template_name = 'messages.html'


class NewTrialView(TemplateView):
    template_name = 'sponsor/newtrial.html'


class TrialsView(TemplateView):
    template_name = 'sponsor/viewtrials.html'


class CriteriaView(TemplateView):
    template_name = 'sponsor/criteria.html'





# Static pages for Admin
# class NewCriterionView(TemplateView):
#     template_name = 'new_criterion.html'
#
# class ViewCriteriaView(TemplateView):
#     template_name = 'view_criteria.html'

class NewSponsorView(generic.CreateView):
    model = Sponsor

    fields = ('organization', 'contactPerson', 'location', 'phone', 'email', 'notes')
    template_name = 'sponsor/new_sponsor.html'


class NewClinicalTrialView(generic.CreateView):
    model = ClinicalTrial
    fields = (
        'id', 'sponsor', 'title', 'objective', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget', 'url',
        'followUp', 'location', 'comments')
    template_name = 'sponsor/newtrial.html'


class ViewSponsorView(TemplateView):
    template_name = 'sponsor/view_sponsor.html'


class ViewSponsorReqView(TemplateView):
    template_name = 'sponsor/view_sponsor_req.html'


# NEW: view for clinicaltrial_list2
class ClinicalTrialListView2(SingleTableView):
    model = ClinicalTrial
    template_name = 'sponsor/clinicaltrial_list2.html'
    table_class = ClinicalTrialTable


class TrialView(SingleTableView):
    model = ClinicalTrial
    # template_name = 'sponsor/trial_view_column.html'
    # table_class = ClinicalTrialTable
