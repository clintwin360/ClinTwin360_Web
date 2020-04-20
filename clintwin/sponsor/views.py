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

from rest_framework.decorators import api_view, permission_classes
from .models import Contact, Sponsor, Participant, ClinicalTrial, ClinicalTrialCriteriaResponse, \
    ParticipantQuestion
from django.contrib.auth.models import User
from .serializers import *
from django.core.management import call_command
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import Count

# New
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import ClinicalTrialTable
import ast
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
    return render(request, "sponsor/viewtrials.html",)

class TrialPaneView(generic.DetailView):
    model = ClinicalTrial
    template_name_suffix = '_pane'

class TrialDetailView(generic.DetailView):
    model = ClinicalTrial


class TrialUpdateView(generic.UpdateView):
    model = ClinicalTrial
    fields = '__all__'
    def get_success_url(self):
          trialid=self.kwargs['pk']
          return reverse_lazy('trialdetail', kwargs={'pk': trialid})

class TrialUpdatePaneView(generic.UpdateView):
    model = ClinicalTrial
    fields = '__all__'
    template_name_suffix = '_update_pane'
    success_url = reverse_lazy('viewtrials')

# NEW
def TrialStartView(request, pk):
	trial = ClinicalTrial.objects.get(pk=pk)
	if trial.status != 'Started':
	   trial.status = 'Started'
	   trial.save(update_fields=['status'])

	   #return reverse_lazy('viewtrials')
	   return redirect("viewtrials")

#NEW

	   #return render("viewtrials")
	   #return render(request, "sponsor/viewtrials.html", context)
	   #reverse('sponsor : viewtrials')
	   #return reverse_lazy('trialdetail', kwargs={'pk': pk})
	   #return HttpResponseRedirect(reverse('viewtrials'))


#NEW

def TrialEndView(request, pk):
	trial = ClinicalTrial.objects.get(pk=pk)
	if trial.status == 'Started':
	   trial.status = 'Ended'
	   trial.save(update_fields=['status'])

	   #return reverse_lazy('viewtrials')
	   return redirect("viewtrials")



class DeleteTrialView(generic.DeleteView):
    model = ClinicalTrial
    success_url = reverse_lazy('viewtrials')

class DeleteTrialPaneView(generic.DeleteView):
    model = ClinicalTrial
    success_url = reverse_lazy('viewtrials')
    template_name_suffix = '_delete_pane'

class NewClinicalTrialView(generic.CreateView):
    model = ClinicalTrial
    fields = (
        'custom_id', 'title', 'sponsor', 'objective', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget', 'url',
        'followUp', 'location', 'comments')
    template_name = 'sponsor/newtrial.html'
    success_url = reverse_lazy('viewtrials')

    def get_initial(self, *args, **kwargs):
        if not (self.request.user.is_clintwin()):
            initial = {}
            initial['sponsor'] = self.request.user.profile.sponsor
            return initial
        else:
            return self.initial.copy()


    #def get_form(self):
    #    print(self.request.POST)
    #    self.object = self.get_object()
    #    return self.form_class(for_list=self.object, data=self.request.POST)


#Sponsor Views
def viewSponsors(request):
    queryset = Sponsor.objects.all()
    return render(request, "sponsor/view_sponsors.html")


class SponsorDetailView(generic.DetailView):
    model = Sponsor


class SponsorUpdateView(generic.UpdateView):
    model = Sponsor
    fields = '__all__'

    def get_success_url(self):
          sponsorid=self.kwargs['pk']
          return reverse_lazy('sponsordetail', kwargs={'pk': sponsorid})


class DeleteSponsorView(generic.DeleteView):
    model = Sponsor
    success_url = reverse_lazy('viewsponsors')


class NewSponsorView(generic.CreateView):
    model = Sponsor
    fields = ['organization', 'contactPerson', 'location', 'phone', 'email', 'notes']
    template_name = 'sponsor/new_sponsor.html'
    success_url = reverse_lazy('viewsponsors')

#Other views
def compare_values(a, op, b):
    if op == "equals":
        return a == b
    if op == 'gte':
        return float(a) >= float(b)
    if op == 'lte':
        return float(a) <= float(b)


def calculate_trial_matches(participant):
    #participant = Participant.objects.get(id=1)
    responses = participant.responses.all()
    current_matches = [x.clinical_trial.id for x in participant.trial_matches.select_related('clinical_trial')]
    trials = ClinicalTrial.objects.all().exclude(id__in=current_matches)
    #return JsonResponse({"data": [x.title for x in trials]})
    new_matches = 0
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
                if responses.filter(question__id=question.id).exists():
                    response = responses.get(question__id=question.id)
                else:
                    response = None
                if not response:
                    trial_match = False
                    continue
                else:
                    response_value = response.value
                    value_match = compare_values(response_value, comparison, criterion_value)
                    if value_match and criterion_type == "inclusion" or not value_match and criterion_type == "exclusion":
                        continue
                    else:  # this will not match if value_match is not true or if type is exclusion, we may want to separate cases
                        trial_match = False
                        continue
        if trial_match:
            ClinicalTrialMatch.objects.create(participant=participant, clinical_trial=trial, match=True)
            new_matches += 1
        else:
            ClinicalTrialMatch.objects.create(participant=participant, clinical_trial=trial, match=False)
    #return JsonResponse({"data": new_matches})
    return new_matches


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
    participant_id = request.GET.get('participant_id')
    questions = ParticipantQuestion.objects.all()
    if participant_id:
        print("WE PARTICPANT {}".format(participant_id))
        responses = ParticipantResponse.objects.filter(participant__id=participant_id)
        answered_questions = [x.question.id for x in responses]
        questions = questions.exclude(id__in=answered_questions)

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
                                  'options': ast.literal_eval(question.options),
                                  'followups':
                                      [{'response': x.response, 'next_question': x.next_question.id} for x in flow]})
    return JsonResponse(data)


def load_data(request):
    call_command('loaddata', 'participant_questions')
    call_command('loaddata', 'groups')
    call_command('loaddata', 'users')
    call_command('loaddata', 'participants')
    call_command('loaddata', 'trial_criteria')
    call_command('loaddata', 'sponsors')
    call_command('loaddata', 'clinical_trials')
    call_command('loaddata', 'criteria_responses')
    call_command('loaddata', 'trial_matches')
    call_command('loaddata', 'participant_responses')
    call_command('loaddata', 'question_flow')
    call_command('loaddata', 'user_profiles')
    return HttpResponse("Data Loaded!")


# View for contact us form
#@api_view(['GET, POST'])
@permission_classes((permissions.AllowAny,))
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

def viewSponsorReq(request):
    query_results = SponsorRequest.objects.all()
    return render(request, "sponsor/view_sponsor_req.html")

# Supplementary Views
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

def emptyPane(request):
    return render(request, "sponsor/emptypane.html",)
# Static pages for Admin
# class NewCriterionView(TemplateView):
#     template_name = 'new_criterion.html'
#
# class ViewCriteriaView(TemplateView):
#     template_name = 'view_criteria.html'

# Test views
def dummy(request):
    return render(request, 'sponsor/dummy.html')


def criteria_investigation(request):
    return render(request, 'sponsor/criteria_investigation.html')

class ViewSponsorView(TemplateView):
    template_name = 'sponsor/view_sponsor.html'


class ViewSponsorReqView(TemplateView):
    template_name = 'sponsor/view_sponsor_req.html'


# NEW: view for clinicaltrial_list2
class ClinicalTrialListView2(SingleTableView):
    model = ClinicalTrial
    template_name = 'sponsor/clinicaltrial_list2.html'
    table_class = ClinicalTrialTable
