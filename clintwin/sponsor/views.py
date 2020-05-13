##  Original additions
# New
import ast
import csv  # NEW
import io
from datetime import timedelta
from abc import ABC

from bootstrap_datepicker_plus import DatePickerInput
from django.contrib import messages  # NEW
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.forms import CheckboxInput
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
# from .forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

# from .forms import *
from sponsor.forms import NewAccountSponsorAdminForm
from .serializers import *

# New additions

# Create your views here.


# hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
# if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):


# Hardcoding this stuff for now, but this needs to be derived from the data model
QUESTION_EXCLUDES = [1, 2, 3, 5, 87]
FEMALE_QUESTIONS = [10, 38]


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
        next_page = "/sponsor/trial/{}/question_upload/".format(trial.id)
        next_page_text = "Continue"
    else:
        next_page = "/sponsor/dashboard/"
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


@login_required
def question_upload(request, pk):
    trial = ClinicalTrial.objects.get(pk=pk)
    print(trial)
    # declaring template
    template = 'sponsor/question_upload.html'
    data = {'order': 'order of CSV should be text, valueType, options', 'clinicaltrial': trial}

    # Handle the GET model
    if request.method == "GET":
        return render(request, template, data)
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
            clinical_trial = trial
            text = column[1]
            valueType = column[2]
            options = column[3].replace(";", ",").replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"',
                                                                                                                   '}').replace(
                '""', '"')
            frequency = timedelta(int(column[4]))

            vtquestion = VirtualTrialParticipantQuestion.objects.create(
                clinical_trial=clinical_trial, text=text, valueType=valueType, options=options, frequency=frequency)
        vtquestion.save()
        vtquestions = VirtualTrialParticipantQuestion.objects.all().filter(clinical_trial=pk)
        context = {}
        messages.success(request, "Succesfully uploaded trial questions from file: " + csv_file.name)

    # Else if problem with files
    else:
        messages.error(request, "Problem with uploaded file's format")

    return render(request, template, {"vtquestions": vtquestions})


@login_required
def login_success(request):
    if request.user.groups.filter(name='clintwin'):
        return redirect("viewsponsors")
    elif request.user.groups.filter(name='sponsor'):
        return render(request, "sponsor/trial_dashboard.html")
    else:
        logout(request)
        return redirect('index')


class TrialUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ClinicalTrial
    fields = '__all__'

    def get_form(self, form_class=None):
        print(self.request);
        form = super().get_form()
        form.fields['recruitmentStartDate'].widget = DatePickerInput(format='%m/%d/%Y')
        form.fields['recruitmentEndDate'].widget = DatePickerInput(format='%m/%d/%Y')
        form.fields['is_virtual'].widget = CheckboxInput()
        return form

    def get_success_url(self):
        return reverse_lazy('trial_dashboard')




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
            initial['sponsor'] = self.request.user.sponsor_profile.sponsor
            return initial
        else:
            return self.initial.copy()


# Sponsor Views
class SponsorListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Sponsor
    pagination_by = 25

    ordering = ['organization']

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


class SponsorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sponsor


class SponsorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Sponsor
    fields = '__all__'

    def get_success_url(self):
        sponsorid = self.kwargs['pk']
        return reverse_lazy('sponsordetail', kwargs={'pk': sponsorid})

    def test_func(self):
        return (self.request.user.groups.filter(name='clintwin').exists() or self.request.user.groups.filter(name='sponsor_admin').exists())


class DeleteSponsorView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Sponsor
    success_url = reverse_lazy('viewsponsors')

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


class NewSponsorView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
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

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        sponsorid = self.object.id
        return redirect(reverse_lazy('sponsordetail', kwargs={'pk': sponsorid}))


class NewSponsorFillView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView, ABC):
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

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


# Account Views
class NewAccountView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = User

    form_class = NewAccountSponsorAdminForm
    template_name = 'sponsor/new_account.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        sponsor_id = self.request.session['sponsor_id']
        self.object.save()
        sponsor_admin_group = Group.objects.get(name='sponsor_admin')
        sponsor_admin_group.user_set.add(self.object)
        sponsor_group = Group.objects.get(name='sponsor')
        sponsor_group.user_set.add(self.object)
        UserProfile.objects.get_or_create(user=self.object, sponsor=Sponsor.objects.get(pk=sponsor_id))
        if not self.object.has_usable_password():
            self.request.session['email'] = self.object.email
            return redirect('passwordemail')
        else:
            return redirect(reverse_lazy('viewaccount', kwargs={'pk': self.object.id}))

    def get_form(self):
        form = super().get_form()
        form.fields['username'].widget.attrs['placeholder'] = 'Username for the account'
        form.fields['email'].widget.attrs['placeholder'] = 'Email associated to the account'
        form.fields['first_name'].widget.attrs['placeholder'] = 'First name of user associated to the account'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Last name of user associated to the account'
        return form

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


class NewAccountSponsorAdminView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = User

    form_class = NewAccountSponsorAdminForm
    template_name = 'sponsor/new_account_sa.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        sponsor_id = self.request.session['sponsor_admin_id']
        self.object.save()
        sponsor_group = Group.objects.get(name='sponsor')
        sponsor_group.user_set.add(self.object)
        UserProfile.objects.get_or_create(user=self.object, sponsor=Sponsor.objects.get(pk=sponsor_id))
        if not self.object.has_usable_password():
            self.request.session['email'] = self.object.email
            return redirect('passwordemail')
        else:
            return redirect(reverse_lazy('viewaccount', kwargs={'pk': self.object.id}))

    def test_func(self):
        return self.request.user.groups.filter(name='sponsor_admin').exists()

    def get_form(self):
        form = super().get_form()
        form.fields['username'].widget.attrs['placeholder'] = 'Username for the account'
        form.fields['email'].widget.attrs['placeholder'] = 'Email associated to the account'
        form.fields['password1'].widget.attrs['placeholder'] = 'Enter a secure password'
        form.fields['password2'].widget.attrs['placeholder'] = 'Enter the same password'
        form.fields['first_name'].widget.attrs['placeholder'] = 'First name of user associated to the account'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Last name of user associated to the account'
        return form


class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'sponsor/account_detail.html'
    context_object_name = 'user_object'


@login_required
def PasswordEmailView(request):
    reset_form = PasswordResetForm({'email': request.session['email']})
    if reset_form.is_valid():
        reset_form.save(
            email_template_name='registration/account_creation_email.html',
            subject_template_name='registration/account_creation_subject.txt',
            # from_email='clintwin@gmail.com',
            request=request
        )
        print('bye')
    if request.user.is_clintwin():
        return redirect('viewsponsors')
    else:
        return redirect('trial_dashboard')


@login_required
def NewAccountFromSponsor(request, pk):
    sponsor = Sponsor.objects.get(pk=pk)
    request.session['sponsor_id'] = sponsor.id

    return redirect("newaccount")


@login_required
def NewAccountFromSponsorAdmin(request):
    sponsor = request.user.sponsor_profile.sponsor
    request.session['sponsor_admin_id'] = sponsor.id

    return redirect("newaccountsponsoradmin")


# Request Views
class SponsorRequestListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = SponsorRequest
    pagination_by = 25

    ordering = ['-status', '-createdAt']

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


class SponsorRequestDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = SponsorRequest

    def test_func(self):
        return self.request.user.groups.filter(name='sponsor_admin').exists()


class NewSponsorRequestView(LoginRequiredMixin, generic.CreateView):
    model = SponsorRequest
    fields = ['sponsor', 'criterion_req', 'values', 'notes']
    template_name = 'sponsor/request_criteria.html'
    success_url = reverse_lazy('trial_dashboard')

    def get_initial(self, *args, **kwargs):
        if not (self.request.user.is_clintwin()):
            initial = {}
            initial['sponsor'] = self.request.user.sponsor_profile.sponsor
            return initial
        else:
            return self.initial.copy()

    def get_form(self):
        form = super().get_form()
        form.fields['criterion_req'].widget.attrs['placeholder'] = 'Eligibility criteria you would like added'
        form.fields['values'].widget.attrs['placeholder'] = 'A comma-separated list of potential values'
        form.fields['notes'].widget.attrs['placeholder'] = 'Any addtional notes about the criteria'
        return form


class ContactListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Contact
    pagination_by = 25

    ordering = ['-status', '-createdAt']

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Contact

    def test_func(self):
        return self.request.user.groups.filter(name='clintwin').exists()


class ContactPageView(generic.CreateView):
    model = Contact
    fields = ['organization', 'location', 'first_name', 'last_name', 'email', 'phone', 'comment']
    template_name = 'sponsor/contact.html'
    success_url = reverse_lazy('index')

    def get_form(self):
        form = super().get_form()
        form.fields['organization'].widget.attrs['placeholder'] = 'Name of the sponsor organization'
        form.fields['location'].widget.attrs['placeholder'] = 'Location of the sponsor organization'
        form.fields['first_name'].widget.attrs['placeholder'] = "Enter first name"
        form.fields['last_name'].widget.attrs['placeholder'] = "Enter last name"
        form.fields['email'].widget.attrs['placeholder'] = "Enter email address"
        form.fields['phone'].widget.attrs['placeholder'] = "Enter phone number"
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
    # update age:
    age_response = participant.responses.get(question__id=3)
    age_response.value = participant.basic_health.age()
    age_response.save()

    responses = participant.responses.all()
    current_matches = [x.clinical_trial.id for x in participant.trial_matches.select_related('clinical_trial')]
    trials = ClinicalTrial.objects.filter(status="Active Recruitment").exclude(id__in=current_matches)
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
    questions = ParticipantQuestion.objects.all().exclude(id__in=QUESTION_EXCLUDES)
    if participant_id:
        basic_health = ParticipantBasicHealth.objects.get(participant__id=participant_id)
        sex = basic_health.sex
        if sex == "M":
            questions = questions.exclude(id__in=FEMALE_QUESTIONS)
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


def calculate_virtual_tasks(participant,clinical_trial):
    virtual_questions = clinical_trial.virtual_questions.all()
    virtual_responses = participant.virtual_responses.all()
    current_questions = []
    for vq in virtual_questions:
        responses_for_q = virtual_responses.filter(question=vq).order_by('-last_answered')
        if responses_for_q.count() > 0:
            last_answered = responses_for_q[0].last_answered
            response_delta = now - last_answered;
            q_frequency = vq.frequency
            if response_delta > q_frequency:
                current_questions.append(vq.id)
        else:
            current_questions.append(vq.id)
    return current_questions


def load_data(request):
    # call_command('loaddata', 'virtualtrial_participant_questions')
    call_command('loaddata', 'participant_questions')
    call_command('loaddata', 'groups')
    call_command('loaddata', 'users')
    call_command('loaddata', 'participants')
    call_command('loaddata', 'participant_profiles')
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


# Supplementary Views
# Static page for About us
class AboutPageView(TemplateView):
    template_name = 'sponsor/about.html'


# Static page for How it Works
class HowWorksPageView(TemplateView):
    template_name = 'sponsor/how_works.html'
