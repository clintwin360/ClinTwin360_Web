from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from sponsor.serializers import *
from sponsor.models import *
from sponsor.views import calculate_trial_matches
from rest_framework import viewsets, mixins
from rest_framework import permissions
from django.contrib.auth import get_user
from django_filters.rest_framework import DjangoFilterBackend

from sponsor.models import Participant

from sponsor.serializers import ParticipantSerializer


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
    queryset = VirtualTrialParticipantQuestion.objects.all()
    serializer_class = VirtualTrialParticipantQuestionSerializer
    # permission_classes = [permissions.IsAuthenticated]


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
        obj = queryset.get(email=self.request.user.email)
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
        basic_health = serializer.save()
        print(basic_health)
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


class ClinicalTrialMatchViewSet(mixins.ListModelMixin,
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
            queryset = ClinicalTrialMatch.objects.none()

        return queryset


class ClinicalTrialViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    List all Clinical Trials or List trials by sponsor_id
    """
    serializer_class = ClinicalTrialListSerializer

    def get_queryset(self):
        sponsor_id = self.request.query_params.get('sponsor_id', None)
        if sponsor_id:
            queryset = ClinicalTrial.objects.filter(sponsor__id=sponsor_id)
        else:
            queryset = ClinicalTrial.objects.all()

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
