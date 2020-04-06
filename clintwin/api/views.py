from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer
from sponsor.serializers import *
from sponsor.models import *
from rest_framework import viewsets
from rest_framework import permissions


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


# API
class ParticipantQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = ParticipantQuestion.objects.all()
    serializer_class = ParticipantQuestionSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be viewed or edited.
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ParticipantBasicHealthViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be viewed or edited.
    """
    queryset = ParticipantBasicHealth.objects.all()
    serializer_class = ParticipantBasicHealthSerializer

    def perform_create(self, serializer):
        basic_health = serializer.save()
        print(basic_health)
    # permission_classes = [permissions.IsAuthenticated]


class ParticipantResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows responses to be viewed or edited.
    """
    queryset = ParticipantResponse.objects.all()
    serializer_class = ParticipantResponseSerializer
    # permission_classes = [permissions.IsAuthenticated]


class SponsorProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows responses to be viewed or edited.
    """
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ClinicalTrialMatchViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalTrialMatchSerializer

    def get_queryset(self):
        participant_id = self.request.query_params.get('participant')
        participant = Participant.objects.get(id=participant_id)
        queryset = ClinicalTrialMatch.objects.filter(participant=participant)

        return queryset


class ClinicalTrialDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalTrialDetailSerializer

    def get_queryset(self):
        trial_id = self.request.query_params.get('id')
        queryset = ClinicalTrial.objects.filter(id=trial_id)

        return queryset


class ClinicalTrialViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalTrialListSerializer

    def get_queryset(self):
        sponsor_id = self.request.query_params.get('sponsor_id', None)
        if sponsor_id:
            queryset = ClinicalTrial.objects.filter(sponsor__id=sponsor_id)
        else:
            queryset = ClinicalTrial.objects.all()

        return queryset
