##  Original additions
import csv, io #NEW
from django.contrib import messages #NEW
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from django.views.generic import TemplateView

from django.forms import PasswordInput
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
from django.contrib.auth import views as auth_views, logout
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import Count

# New
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import ClinicalTrialTable
import ast
from rest_framework import pagination

from bootstrap_datepicker_plus import DatePickerInput
from django.forms import fields, CheckboxInput
from django.core.exceptions import ValidationError


# Create your views here.


# hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
# if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return login_success(request)


@login_required
def trial_dashboard(request):
    trials = ClinicalTrial.objects.filter()
    return render(request, 'sponsor/trial_dashboard.html')


# Updated to post trial criteria to API endpoint
@login_required
def trial_criteria(request, pk, criteria_type):
    trial = ClinicalTrial.objects.get(pk=pk)
    if criteria_type == "inclusion":
        next_page = "/sponsor/trial/{}/criteria/exclusion/".format(trial.id)
        next_page_text = "Exclusion Criteria"
        previous_page = "/sponsor/updatetrial/{}".format(trial.id)
        previous_page_text = "Edit Trial"
    else:
        next_page = "/sponsor/trial/{}/criteria/review/".format(trial.id)
        next_page_text = "Review Criteria"
        previous_page = "/sponsor/trial/{}/criteria/inclusion/".format(trial.id)
        previous_page_text = "Inclusion Criteria"

    trial_criteria_responses = ClinicalTrialCriteriaResponse.objects.all().filter(trial=pk, criteriaType=criteria_type)
    return render(request, "sponsor/trial_criteria.html",
                  {"trial_criteria": trial_criteria_responses,
                   "clinicaltrial": trial, "criteria_type": criteria_type,
                   "previous_page": previous_page, "next_page": next_page,
                   "previous_page_text": previous_page_text,
                   "next_page_text": next_page_text})

@login_required
def review_criteria(request, pk):
    trial = ClinicalTrial.objects.get(pk=pk)
    trial_criteria_responses = ClinicalTrialCriteriaResponse.objects.all().filter(trial=pk)
    inclusion_criteria = trial_criteria_responses.filter(criteriaType="inclusion")
    exclusion_criteria = trial_criteria_responses.filter(criteriaType="exclusion")

    if trial.is_virtual:
        next_page = "/sponsor/trial/{}/vt_question_upload/".format(trial.id)
        next_page_text = "Continue"
    else:
        next_page = "/sponsor/viewtrials"
        next_page_text = "Continue"

    previous_page = "/sponsor/trial/{}/criteria/exclusion/".format(trial.id)
    previous_page_text = "Exclusion Criteria"

    return render(request, "sponsor/review_criteria.html",
                  {"inclusion_criteria": inclusion_criteria,
                   "exclusion_criteria": exclusion_criteria,
                   "clinicaltrial": trial,
                   "previous_page": previous_page, "next_page": next_page,
                   "previous_page_text": previous_page_text,
                   "next_page_text": next_page_text})


# def vt_question_upload(request):
#     return render(request, 'sponsor/vt_question_upload.html')
@login_required
def vt_question_upload(request, pk):
    trial = ClinicalTrial.objects.get(pk=pk)
    # declaring template
    template = 'sponsor/vt_question_upload.html'
    prompt = {'order': 'order of CSV should be text, valueType, options'
    }

    # Handle the GET model
    if request.method == "GET":
        return render(request, template, prompt)
    # Handle the POST model
    if request.method == "POST":
        csv_file = request.FILES['fileUploaded']

        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            trial_id = trial
            text = column[1]
            valueType=column[2]
            options = column[3].replace(";",",").replace('"[','[').replace(']"',']').replace('"{','{').replace('}"','}').replace('""', '"')

            vtquestion = VirtualTrialParticipantQuestion.objects.create(
                trial_id=trial_id, text=text, valueType=valueType, options=options)
        vtquestion.save()
        vtquestions = VirtualTrialParticipantQuestion.objects.all().filter(trial_id=pk)
        context = {}
        messages.success(request, "Succesfully uploaded trial questions from file: " + csv_file.name)

    # Else if problem with files
    else:
        messages.error(request, "Problem with uploaded file's format")

    return render(request, template, {"vtquestions" : vtquestions})

@login_required
def login_success(request):
    if request.user.groups.filter(name='clintwin'):
        return redirect("viewsponsors")
    elif request.user.groups.filter(name='sponsor'):
        return render(request, "sponsor/trial_dashboard.html")
    else:
        logout(request)
        return redirect('index')



# Trial Views
@login_required
def viewTrials(request):
    return render(request, "sponsor/viewtrials.html")


class TrialPaneView(LoginRequiredMixin, generic.DetailView):
    model = ClinicalTrial
    template_name_suffix = '_pane'


class TrialDetailView(LoginRequiredMixin, generic.DetailView):
    model = ClinicalTrial


class TrialUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ClinicalTrial
    fields = '__all__'

    def get_form(self):

         form = super().get_form()
         form.fields['recruitmentStartDate'].widget = DatePickerInput(format='%m/%d/%Y')
         form.fields['recruitmentEndDate'].widget = DatePickerInput(format='%m/%d/%Y')
         form.fields['is_virtual'].widget = CheckboxInput()
         return form


    def get_success_url(self):
        trialid = self.kwargs['pk']
        return reverse_lazy('trialdetail', kwargs={'pk': trialid})


class TrialUpdatePaneView(LoginRequiredMixin, generic.UpdateView):
    model = ClinicalTrial
    fields = '__all__'

    def get_form(self):

         form = super().get_form()
         form.fields['recruitmentStartDate'].widget = DatePickerInput(format='%m/%d/%Y')
         form.fields['recruitmentEndDate'].widget = DatePickerInput(format='%m/%d/%Y')
         form.fields['is_virtual'].widget = CheckboxInput()
         return form

    template_name_suffix = '_update_pane'
    success_url = reverse_lazy('viewtrials')


# NEW
@login_required
def TrialStartView(request, pk):
    trial = ClinicalTrial.objects.get(pk=pk)
    if trial.status != 'Started':
        trial.status = 'Started'
        trial.save(update_fields=['status'])

        # return reverse_lazy('viewtrials')
        return redirect("viewtrials")


# NEW

# return render("viewtrials")
# return render(request, "sponsor/viewtrials.html", context)
# reverse('sponsor : viewtrials')
# return reverse_lazy('trialdetail', kwargs={'pk': pk})
# return HttpResponseRedirect(reverse('viewtrials'))


# NEW
@login_required
def TrialEndView(request, pk):
    trial = ClinicalTrial.objects.get(pk=pk)
    if trial.status == 'Started':
        trial.status = 'Ended'
        trial.save(update_fields=['status'])

        # return reverse_lazy('viewtrials')
        return redirect("viewtrials")


class NewClinicalTrialView(LoginRequiredMixin, generic.CreateView):
    model = ClinicalTrial
    fields = (
        'custom_id', 'title', 'is_virtual', 'sponsor', 'objective', 'recruitmentStartDate', 'recruitmentEndDate',
        'enrollmentTarget', 'url',
        'followUp', 'location', 'comments')

    template_name = 'sponsor/newtrial.html'

    def get_success_url(self, **kwargs):
        return "/sponsor/trial/{}/criteria/inclusion/".format(self.object.pk)

    def get_form(self):
        form = super().get_form()
        form.fields['custom_id'].widget.attrs['placeholder'] = 'Enter the trial ID'
        form.fields['title'].widget.attrs['placeholder'] = 'Enter the title of the trial'
        form.fields['objective'].widget.attrs['placeholder'] = 'Describe in brief detail the objective of this trial'
        form.fields['enrollmentTarget'].widget.attrs['placeholder'] = 'The enrollment target for this trial'
        form.fields['url'].widget.attrs['placeholder'] = 'Enter a URL link to any external trial page'
        form.fields['location'].widget.attrs['placeholder'] = 'The location of this trial'
        form.fields['recruitmentStartDate'].widget = DatePickerInput(format='%m/%d/%Y')
        form.fields['recruitmentEndDate'].widget = DatePickerInput(format='%m/%d/%Y')
        form.fields['is_virtual'].widget = CheckboxInput()
        return form

    def get_initial(self, *args, **kwargs):
        if not (self.request.user.is_clintwin()):
            initial = {}
            initial['sponsor'] = self.request.user.profile.sponsor
            return initial
        else:
            return self.initial.copy()

    # def get_form(self):
    #    print(self.request.POST)
    #    self.object = self.get_object()
    #    return self.form_class(for_list=self.object, data=self.request.POST)


# Sponsor Views
@login_required
def viewSponsors(request):
    queryset = Sponsor.objects.all()
    return render(request, "sponsor/view_sponsors.html")


class SponsorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sponsor


class SponsorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Sponsor
    fields = '__all__'

	#Datepicker widet below throws weird indent error
    #def get_form(self):
	    #form = super().get_form()
        #form.fields['dateDeregistered'].widget = DatePickerInput(format='%m/%d/%Y')
		#return form

    def get_success_url(self):
        sponsorid = self.kwargs['pk']
        return reverse_lazy('sponsordetail', kwargs={'pk': sponsorid})


class DeleteSponsorView(LoginRequiredMixin, generic.DeleteView):
    model = Sponsor
    success_url = reverse_lazy('viewsponsors')


class NewSponsorView(LoginRequiredMixin, generic.CreateView):
    model = Sponsor
    fields = ['organization', 'contactPerson', 'location', 'phone', 'email', 'notes']

    template_name = 'sponsor/new_sponsor.html'
    success_url = reverse_lazy('viewsponsors')

    def get_form(self):
        form = super().get_form()
        form.fields['organization'].widget.attrs['placeholder'] = 'Name of the sponsor organization'
        form.fields['contactPerson'].widget.attrs['placeholder'] = 'Name of the contact person'
        form.fields['location'].widget.attrs['placeholder'] = 'Where the organization is located'
        form.fields['phone'].widget.attrs['placeholder'] = 'Phone number'
        form.fields['email'].widget.attrs['placeholder'] = 'Email address'
        form.fields['notes'].widget.attrs['placeholder'] = 'Enter any relevant notes about the sponsor here'
        return form


class NewSponsorFillView(LoginRequiredMixin, generic.CreateView):
    model = Sponsor
    fields = ['organization', 'contactPerson', 'location', 'phone', 'email', 'notes']

    template_name = 'sponsor/new_sponsor.html'
    success_url = reverse_lazy('viewsponsors')

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()
        initial = self.request.session['data']
        return initial

    def get_form(self):
        form = super().get_form()
        form.fields['organization'].widget.attrs['placeholder'] = 'Name of the sponsor organization'
        form.fields['contactPerson'].widget.attrs['placeholder'] = 'Name of the contact person'
        form.fields['location'].widget.attrs['placeholder'] = 'Where the organization is located'
        form.fields['phone'].widget.attrs['placeholder'] = 'Phone number'
        form.fields['email'].widget.attrs['placeholder'] = 'Email address'
        form.fields['notes'].widget.attrs['placeholder'] = 'Enter any relevant notes about the sponsor here'
        return form

#Account Views
class NewAccountView(LoginRequiredMixin, generic.CreateView):
    model = User
    fields = ['username', 'password', 'email', 'first_name', 'last_name',]

    template_name = 'sponsor/new_account.html'
    success_url = reverse_lazy('viewsponsors')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        sponsor_id = self.request.session['id']
        self.object.save()
        UserProfile.objects.get_or_create(user=self.object, sponsor=Sponsor.objects.get(pk=sponsor_id))
        return redirect(self.get_success_url())


    def get_form(self):
        form = super().get_form()
        form.fields['username'].widget.attrs['placeholder'] = 'Username for the account'
        form.fields['password'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a secure password'})
        form.fields['email'].widget.attrs['placeholder'] = 'Email address for the account'
        form.fields['first_name'].widget.attrs['placeholder'] = 'First name of the user'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Last name of the user'
        return form

class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'sponsor/account_detail.html'


@login_required
def NewAccountFromSponsor(request, pk):
    sponsor = Sponsor.objects.get(pk=pk)
    request.session['id'] = sponsor.id

    return redirect("newaccount")


# Request Views
@login_required
def viewSponsorReq(request):
    return render(request, "sponsor/view_sponsor_req.html")


class SponsorRequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = SponsorRequest


class NewSponsorRequestView(LoginRequiredMixin, generic.CreateView):
    model = SponsorRequest
    fields = ['sponsor', 'criterion_req', 'values', 'notes']
    template_name = 'sponsor/request_criteria.html'
    success_url = reverse_lazy('viewtrials')

    def get_initial(self, *args, **kwargs):
        if not (self.request.user.is_clintwin()):
            initial = {}
            initial['sponsor'] = self.request.user.profile.sponsor
            return initial
        else:
            return self.initial.copy()

    def get_form(self):
        form = super().get_form()
        form.fields['criterion_req'].widget.attrs['placeholder'] = 'Eligibility criteria you would like added'
        form.fields['values'].widget.attrs['placeholder'] = 'A comma-separated list of potential values'
        form.fields['notes'].widget.attrs['placeholder'] = 'Any addtional notes about the criteria'
        return form


class ContactListView(LoginRequiredMixin, generic.ListView):
    model = Contact
    pagination_by = 25


class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contact


class ContactPageView(generic.CreateView):

        model = Contact
        fields = ['organization', 'location', 'first_name', 'last_name', 'email', 'phone' ,'comment']
        template_name = 'sponsor/contact.html'
        success_url = reverse_lazy('index')

        def get_form(self):
            form = super().get_form()
            form.fields['organization'].widget.attrs['placeholder'] = 'Name of the sponsor organization'
            form.fields['location'].widget.attrs['placeholder'] = 'Location of the sponsor organization'
            form.fields['first_name'].widget.attrs['placeholder'] = "Contact's first name"
            form.fields['last_name'].widget.attrs['placeholder'] = "Contact's last name"
            form.fields['email'].widget.attrs['placeholder'] = "Contact's email address"
            form.fields['phone'].widget.attrs['placeholder'] = "Contact's phone number"
            form.fields['comment'].widget.attrs['placeholder'] = 'Any addtional comments about the request'
            return form


@login_required
def CriteriaRequestCompleteView(request, pk):
    criteria_request = SponsorRequest.objects.get(pk=pk)
    if criteria_request.status == 'Open':
        criteria_request.status = 'Completed'
        criteria_request.save(update_fields=['status'])

        return redirect("viewsponsorreq")


@login_required
def AccessRequestCloseView(request, pk):
    access_request = Contact.objects.get(pk=pk)
    if access_request.status == 'Open':
        access_request.status = 'Closed'
        access_request.save(update_fields=['status'])

        return redirect("contactlist")


@login_required
def NewSponsorFromRequest(request, pk):
    access_request = Contact.objects.get(pk=pk)
    request.session['data'] = {'organization': access_request.organization,
            'contactPerson': access_request.first_name + " " + access_request.last_name,
            'location': access_request.location,
            'phone': str(access_request.phone),
            'email': access_request.email}

    return redirect("newsponsorfill")


# Other views
def compare_values(a, op, b):
    if op == "equals":
        return a == b
    if op == 'gte':
        return float(a) >= float(b)
    if op == 'lte':
        return float(a) <= float(b)


def calculate_trial_matches(participant):
    # participant = Participant.objects.get(id=1)
    responses = participant.responses.all()
    current_matches = [x.clinical_trial.id for x in participant.trial_matches.select_related('clinical_trial')]
    trials = ClinicalTrial.objects.all().exclude(id__in=current_matches)
    # return JsonResponse({"data": [x.title for x in trials]})
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
    # return JsonResponse({"data": new_matches})
    return new_matches


def question_rank(questions):
    ranks = {}
    for q in questions:
        rank = 0
        criteria = q.criteria.all()
        for criterion in criteria:
            rank += criterion.trial_responses.count()
        ranks[q.id] = rank
    # data['questions'].sort(key=lambda x: x['rank'], reverse=True)
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


@login_required
def load_data(request):
    call_command('loaddata', 'participant_questions')
    # call_command('loaddata', 'virtualtrial_participant_questions')
    call_command('loaddata', 'groups')
    call_command('loaddata', 'users')
    call_command('loaddata', 'participants')
    call_command('loaddata', 'trial_criteria')
    call_command('loaddata', 'sponsors')
    call_command('loaddata', 'clinical_trials')
    call_command('loaddata', 'criteria_responses')
    call_command('loaddata', 'trial_matches')
    call_command('loaddata', 'participant_responses')
    # call_command('loaddata', 'virtualtrial_participant_responses')
    call_command('loaddata', 'question_flow')
    call_command('loaddata', 'user_profiles')
    return HttpResponse("Data Loaded!")


# View for contact us form
# @api_view(['GET, POST'])
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


class ClinicalTrialCreateView(LoginRequiredMixin, generic.CreateView):
    model = ClinicalTrial
    fields = (
        'id', 'sponsorId', 'title', 'objective', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget',
        'url',
        'followUp', 'location', 'comments')
    template_name = 'create_trial_form.html'


# Supplementary Views
# Static page for About us
class AboutPageView(TemplateView):
    template_name = 'sponsor/about.html'


# Static page for How it Works
class HowWorksPageView(TemplateView):
    template_name = 'sponsor/how_works.html'


# Static page for Contact us



# Static page for directions
class DirectionsPageView(TemplateView):
    template_name = 'directions.html'


# Static page for Message display
class MessagePageView(TemplateView):
    template_name = 'messages.html'


def emptyPane(request):
    return render(request, "sponsor/emptypane.html", )


# Static pages for Admin
# class NewCriterionView(TemplateView):
#     template_name = 'new_criterion.html'
#
# class ViewCriteriaView(TemplateView):
#     template_name = 'view_criteria.html'

# Test views

@login_required
def card(request):
    trials = ClinicalTrial.objects.filter()
    return render(request, 'sponsor/card.html')


class ViewSponsorView(LoginRequiredMixin, TemplateView):
    template_name = 'sponsor/view_sponsor.html'
