from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from sponsor.serializers import *
from sponsor.models import *
from sponsor.views import calculate_trial_matches, calculate_virtual_tasks
from rest_framework import viewsets, mixins
from rest_framework import permissions
from django.contrib.auth import get_user
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime


def get_token(request):
    x = get_user(request)
    token = Token.objects.create(user=x)
    return HttpResponse(token)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


# API
class ClinicalTrialCriteriaViewSet(mixins.ListModelMixin,
                                   GenericViewSet):
    """
    retrieve a list of questions
    """
    queryset = ClinicalTrialCriteria.objects.all()
    serializer_class = ClinicalTrialCriteriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['searchable']


class ParticipantQuestionViewSet(mixins.ListModelMixin,
                                 GenericViewSet):
    """
    retrieve a list of questions
    """
    queryset = ParticipantQuestion.objects.all()
    serializer_class = ParticipantQuestionSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VirtualTrialParticipantQuestionViewSet(mixins.ListModelMixin,
                                             GenericViewSet):
    """
    retrieve a list of questions
    """
    serializer_class = VirtualTrialParticipantQuestionSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        clinical_trial_id = self.request.query_params.get('clinical_trial', None)
        if clinical_trial_id:
            clinical_trial = ClinicalTrial.objects.get(id=clinical_trial_id)
        else:
            print("clinical_trial parameter missing")
            return VirtualTrialParticipantQuestion.objects.none()
        if self.request.user.is_participant() and clinical_trial.is_virtual:
            participant = self.request.user.participant_profile.participant
            current_questions = calculate_virtual_tasks(participant, clinical_trial)
            return VirtualTrialParticipantQuestion.objects.filter(id__in=current_questions)
        else:
            return VirtualTrialParticipantQuestion.objects.none()


class ParticipantViewSet(mixins.RetrieveModelMixin,
                         GenericViewSet):
    """
    create, get, or update a participant
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    # permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(email=self.request.user.username)
        return obj


class ParticipantBasicHealthViewSet(mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    GenericViewSet):
    """
    post or update the basic health info for a participant
    """
    queryset = ParticipantBasicHealth.objects.all()
    serializer_class = ParticipantBasicHealthSerializer

    def perform_create(self, serializer):
        participant = self.request.user.participant_profile.participant
        p2 = serializer.validated_data.get('participant', None)
        if p2 != participant:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        basic_health = serializer.save()
        # creating responses for the basic health data for the trial matching
        ParticipantResponse.objects.create(participant=participant,
                                           question=ParticipantQuestion.objects.get(id=3),
                                           value=basic_health.age())
        ParticipantResponse.objects.create(participant=participant,
                                           question=ParticipantQuestion.objects.get(id=1),
                                           value=basic_health.weight)
        ParticipantResponse.objects.create(participant=participant,
                                           question=ParticipantQuestion.objects.get(id=2),
                                           value=basic_health.height)
        ParticipantResponse.objects.create(participant=participant,
                                           question=ParticipantQuestion.objects.get(id=5),
                                           value=basic_health.sex)
        # IF Male, post No to Pregnancy and Birth Control to avoid false non-matches,
        # since they won't be asked those questions
        if basic_health.sex == "M":
            ParticipantResponse.objects.create(participant=participant,
                                               question=ParticipantQuestion.objects.get(id=10),
                                               value="No")
            ParticipantResponse.objects.create(participant=participant,
                                               question=ParticipantQuestion.objects.get(id=38),
                                               value="No")
        ParticipantResponse.objects.create(participant=participant,
                                           question=ParticipantQuestion.objects.get(id=87),
                                           value=basic_health.bmi())
    # permission_classes = [permissions.IsAuthenticated]


class ParticipantResponseViewSet(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 GenericViewSet):
    """
    post or update a participants response to a question
    """
    queryset = ParticipantResponse.objects.all()
    serializer_class = ParticipantResponseSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VirtualTrialParticipantResponseViewSet(mixins.CreateModelMixin,
                                             mixins.UpdateModelMixin,
                                             GenericViewSet):
    """
    post or update a participants response to a question
    """
    queryset = VirtualTrialParticipantResponse.objects.all()
    serializer_class = VirtualTrialParticipantResponseSerializer
    # permission_classes = [permissions.IsAuthenticated]	


class SponsorProfileViewSet(viewsets.ModelViewSet):
    """
    Allow sponsors to be viewed or edited.
    """
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    # permission_classes = [permissions.IsAuthenticated]


class SponsorRequestViewSet(viewsets.ModelViewSet):
    """
    Allow sponsors to be viewed or edited.
    """
    queryset = SponsorRequest.objects.all()
    serializer_class = SponsorRequestSerializer


class ClinicalTrialMatchViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    """
    Get a list of matching trials for a participant
    """
    serializer_class = ClinicalTrialMatchSerializer

    def get_queryset(self):
        participant_id = self.request.query_params.get('participant')
        if participant_id:
            participant = Participant.objects.get(id=participant_id)
            calculate_trial_matches(participant)
            queryset = ClinicalTrialMatch.objects.filter(participant=participant, match=True)
        else:
            #user_email = request.user.email
            #participant = Participant.objects.get(email=user_email)
            #queryset = ClinicalTrialMatch.objects.filter(participant=participant)
            queryset = ClinicalTrialMatch.objects.all()

        return queryset


class ClinicalTrialEnrollmentViewSet(mixins.CreateModelMixin,
                                     mixins.ListModelMixin,
                                     GenericViewSet):
    """
    Enroll in a Virtual Trial or get a list of enrolled trials for a participant
    """
    serializer_class = ClinicalTrialEnrollmentSerializer

    def get_queryset(self):
        if self.request.user.is_participant():
            participant = self.request.user.participant_profile.participant
            queryset = ClinicalTrialEnrollment.objects.filter(participant=participant)
        else:
            queryset = ClinicalTrialEnrollment.objects.none()

        return queryset


class ClinicalTrialViewSet(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    List all Clinical Trials or List trials by sponsor_id
    """
    serializer_class = ClinicalTrialSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'is_virtual']
    ordering_fields = ['title', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget', 'current_recruitment']

    def get_queryset(self):
        if self.request.user.is_clintwin():
            queryset = ClinicalTrial.objects.all()
        elif self.request.user.is_sponsor():
            queryset = ClinicalTrial.objects.filter(sponsor=self.request.user.sponsor_profile.sponsor)
        else:
            queryset = ClinicalTrial.objects.none()
        return queryset


class ClinicalTrialCriteriaResponseViewSet(mixins.CreateModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.DestroyModelMixin,
                                           mixins.RetrieveModelMixin,
                                           mixins.ListModelMixin,
                                           GenericViewSet):
    """
    List all Clinical Trials or List trials by sponsor_id
    """
    serializer_class = ClinicalTrialCriteriaResponseSerializer

    def get_queryset(self):
        trial_id = self.request.query_params.get('trial', None)
        if trial_id:
            queryset = ClinicalTrialCriteriaResponse.objects.filter(trial__id=trial_id)
        else:
            queryset = ClinicalTrialCriteriaResponse.objects.all()

        return queryset


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def logout(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response(status=status.HTTP_200_OK)


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def password_reset(request):
    form = PasswordResetForm()
    form.cleaned_data = request.data
    form.save(get_current_site(request))
    return Response(status=status.HTTP_200_OK)
