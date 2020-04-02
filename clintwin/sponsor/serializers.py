from .models import *
from rest_framework import serializers

class ParticipantQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantQuestion
        fields = ['id', 'text', 'valueType', 'options']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'email']

class ParticipantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantResponse
        fields = ['question', 'participant', 'value']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['organization', 'contactPerson', 'email']

class ClinicalTrialListSerializer(serializers.ModelSerializer):
    sponsor = SponsorDetailSerializer(read_only=True)

    class Meta:
        model = ClinicalTrial
        fields = ['title', 'objective', 'trialId', 'sponsor']

class ClinicalTrialDetailSerializer(serializers.ModelSerializer):
    sponsor = SponsorDetailSerializer(read_only=True)

    class Meta:
        model = ClinicalTrial
        fields = ['title', 'objective', 'description', 'recruitmentStartDate',
                  'recruitmentEndDate', 'trialId', 'sponsor', 'url']

class ClinicalTrialMatchSerializer(serializers.ModelSerializer):
    clinical_trial = ClinicalTrialListSerializer(read_only=True)

    class Meta:
        model = ClinicalTrialMatch
        fields = ['clinical_trial']
